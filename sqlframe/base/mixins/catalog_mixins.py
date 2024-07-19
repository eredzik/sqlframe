import fnmatch
import typing as t

from sqlglot import exp

from sqlframe.base.catalog import (
    DF,
    SESSION,
    CatalogMetadata,
    Column,
    Database,
    Table,
    _BaseCatalog,
)
from sqlframe.base.util import normalize_string, schema_, to_schema


class _BaseInfoSchemaMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    QUALIFY_INFO_SCHEMA_WITH_DATABASE = False
    UPPERCASE_INFO_SCHEMA = False

    def _get_info_schema_table(
        self,
        table_name: str,
        database: t.Optional[str] = None,
        qualify_override: t.Optional[bool] = None,
    ) -> exp.Table:
        table = f"information_schema.{table_name}"
        if self.UPPERCASE_INFO_SCHEMA:
            table = table.upper()
        qualify = (
            qualify_override
            if qualify_override is not None
            else self.QUALIFY_INFO_SCHEMA_WITH_DATABASE
        )
        if qualify:
            if database:
                db = normalize_string(database, from_dialect="input", to_dialect="output")
            else:
                db = self.currentDatabase()
            if not db:
                raise ValueError("Table name must be qualified with a database.")
            table = f"{db}.{table}"
        return exp.to_table(table)


class GetCurrentCatalogFromFunctionMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    CURRENT_CATALOG_EXPRESSION: exp.Expression = exp.func("current_catalog")

    def currentCatalog(self) -> str:
        """Returns the current default catalog in this session.

        .. versionadded:: 3.4.0

        Examples
        --------
        >>> spark.catalog.currentCatalog()
        'spark_catalog'
        """
        return normalize_string(
            self.session._fetch_rows(
                exp.select(self.CURRENT_CATALOG_EXPRESSION), quote_identifiers=False
            )[0][0],
            from_dialect="execution",
            to_dialect="output",
        )


class GetCurrentDatabaseFromFunctionMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    CURRENT_DATABASE_EXPRESSION: exp.Expression = exp.func("current_schema")

    def currentDatabase(self) -> str:
        """Returns the current default schema in this session.

        .. versionadded:: 3.4.0

        Examples
        --------
        >>> spark.catalog.currentDatabase()
        'default'
        """
        return normalize_string(
            self.session._fetch_rows(exp.select(self.CURRENT_DATABASE_EXPRESSION))[0][0],
            from_dialect="execution",
            to_dialect="output",
        )


class SetCurrentCatalogFromUseMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    def setCurrentCatalog(self, catalogName: str) -> None:
        """Sets the current default catalog in this session.

        .. versionadded:: 3.4.0

        Parameters
        ----------
        catalogName : str
            name of the catalog to set

        Examples
        --------
        >>> spark.catalog.setCurrentCatalog("spark_catalog")
        """
        self.session._execute(
            exp.Use(this=exp.parse_identifier(catalogName, dialect=self.session.input_dialect))
        )


class ListDatabasesFromInfoSchemaMixin(_BaseInfoSchemaMixin, t.Generic[SESSION, DF]):
    def listDatabases(self, pattern: t.Optional[str] = None) -> t.List[Database]:
        """
        Returns a t.List of databases available across all sessions.

        .. versionadded:: 2.0.0

        Parameters
        ----------
        pattern : str
            The pattern that the database name needs to match.

            .. versionchanged: 3.5.0
                Adds ``pattern`` argument.

        Returns
        -------
        t.List
            A t.List of :class:`Database`.

        Examples
        --------
        >>> spark.catalog.t.listDatabases()
        [Database(name='default', catalog='spark_catalog', description='default database', ...

        >>> spark.catalog.t.listDatabases("def*")
        [Database(name='default', catalog='spark_catalog', description='default database', ...

        >>> spark.catalog.t.listDatabases("def2*")
        []
        """
        table = self._get_info_schema_table("schemata", qualify_override=False)
        results = self.session._fetch_rows(
            exp.Select().select("schema_name", "catalog_name").from_(table)
        )
        databases = [
            Database(
                name=normalize_string(x[0], from_dialect="execution", to_dialect="output"),
                catalog=normalize_string(x[1], from_dialect="execution", to_dialect="output"),
                description=None,
                locationUri="",
            )
            for x in results
        ]
        if pattern:
            normalized_pattern = normalize_string(
                pattern, from_dialect="input", to_dialect="output", is_pattern=True
            )
            databases = [db for db in databases if fnmatch.fnmatch(db.name, normalized_pattern)]
        return databases


class ListCatalogsFromInfoSchemaMixin(_BaseInfoSchemaMixin, t.Generic[SESSION, DF]):
    def listCatalogs(self, pattern: t.Optional[str] = None) -> t.List[CatalogMetadata]:
        """
        Returns a t.List of databases available across all sessions.

        .. versionadded:: 2.0.0

        Parameters
        ----------
        pattern : str
            The pattern that the database name needs to match.

            .. versionchanged: 3.5.0
                Adds ``pattern`` argument.

        Returns
        -------
        t.List
            A t.List of :class:`Database`.

        Examples
        --------
        >>> spark.catalog.t.listDatabases()
        [Database(name='default', catalog='spark_catalog', description='default database', ...

        >>> spark.catalog.t.listDatabases("def*")
        [Database(name='default', catalog='spark_catalog', description='default database', ...

        >>> spark.catalog.t.listDatabases("def2*")
        []
        """
        table = self._get_info_schema_table("schemata")
        results = self.session._fetch_rows(
            exp.Select().select("catalog_name").from_(table).distinct()
        )
        catalogs = [
            CatalogMetadata(
                name=normalize_string(x[0], from_dialect="execution", to_dialect="output"),
                description=None,
            )
            for x in results
        ]
        if pattern:
            normalized_pattern = normalize_string(
                pattern, from_dialect="input", to_dialect="output", is_pattern=True
            )
            catalogs = [
                catalog for catalog in catalogs if fnmatch.fnmatch(catalog.name, normalized_pattern)
            ]
        return catalogs


class SetCurrentDatabaseFromSearchPathMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    def setCurrentDatabase(self, dbName: str) -> None:
        """
        Sets the current default database in this session.

        .. versionadded:: 2.0.0

        Examples
        --------
        >>> spark.catalog.setCurrentDatabase("default")
        """
        self.session._execute(f'SET search_path TO "{dbName}"')


class SetCurrentDatabaseFromUseMixin(_BaseCatalog, t.Generic[SESSION, DF]):
    def setCurrentDatabase(self, dbName: str) -> None:
        """
        Sets the current default database in this session.

        .. versionadded:: 2.0.0

        Examples
        --------
        >>> spark.catalog.setCurrentDatabase("default")
        """
        dbName = normalize_string(dbName, from_dialect="input", to_dialect="output", is_schema=True)
        schema = to_schema(dbName, dialect=self.session.output_dialect)

        if not schema.catalog:
            schema.set(
                "catalog",
                exp.parse_identifier(self.currentCatalog(), dialect=self.session.output_dialect),
            )
        self.session._execute(exp.Use(this=schema))


class ListTablesFromInfoSchemaMixin(_BaseInfoSchemaMixin, t.Generic[SESSION, DF]):
    def listTables(
        self, dbName: t.Optional[str] = None, pattern: t.Optional[str] = None
    ) -> t.List[Table]:
        """Returns a t.List of tables/views in the specified database.

        .. versionadded:: 2.0.0

        Parameters
        ----------
        dbName : str
            name of the database to t.List the tables.

            .. versionchanged:: 3.4.0
               Allow ``dbName`` to be qualified with catalog name.

        pattern : str
            The pattern that the database name needs to match.

            .. versionchanged: 3.5.0
                Adds ``pattern`` argument.

        Returns
        -------
        t.List
            A t.List of :class:`Table`.

        Notes
        -----
        If no database is specified, the current database and catalog
        are used. This API includes all temporary views.

        Examples
        --------
        >>> spark.range(1).createTempView("test_view")
        >>> spark.catalog.t.listTables()
        [Table(name='test_view', catalog=None, namespace=[], description=None, ...

        >>> spark.catalog.t.listTables(pattern="test*")
        [Table(name='test_view', catalog=None, namespace=[], description=None, ...

        >>> spark.catalog.t.listTables(pattern="table*")
        []

        >>> _ = spark.catalog.dropTempView("test_view")
        >>> spark.catalog.t.listTables()
        []
        """
        if dbName is None and pattern is None:
            database = normalize_string(
                self.currentDatabase(), from_dialect="output", to_dialect="input"
            )
            catalog = normalize_string(
                self.currentCatalog(), from_dialect="output", to_dialect="input"
            )
            schema = schema_(
                db=exp.parse_identifier(database, dialect=self.session.input_dialect),
                catalog=exp.parse_identifier(catalog, dialect=self.session.input_dialect),
            )
        elif dbName:
            dbName = normalize_string(dbName, from_dialect="input", is_schema=True)
            schema = to_schema(dbName, dialect=self.session.input_dialect)
        else:
            schema = None
        table = self._get_info_schema_table("tables", database=schema.db if schema else None)
        select = exp.select(
            'table_name AS "table_name"',
            'table_schema AS "table_schema"',
            'table_catalog AS "table_catalog"',
            'table_type AS "table_type"',
        ).from_(table)
        if schema and schema.db:
            select = select.where(
                exp.column("table_schema").eq(
                    normalize_string(
                        schema.db,
                        from_dialect="input",
                        to_dialect="execution",
                        to_string_literal=True,
                    )
                )
            )
        if schema and schema.catalog:
            select = select.where(
                exp.column("table_catalog").eq(
                    normalize_string(
                        schema.catalog,
                        from_dialect="input",
                        to_dialect="execution",
                        to_string_literal=True,
                    )
                )
            )
        results = self.session._fetch_rows(select)
        tables = [
            Table(
                name=normalize_string(
                    x["table_name"], from_dialect="execution", to_dialect="output"
                ),
                catalog=normalize_string(
                    x["table_catalog"], from_dialect="execution", to_dialect="output"
                ),
                namespace=[
                    normalize_string(
                        x["table_schema"], from_dialect="execution", to_dialect="output"
                    )
                ],
                description=None,
                tableType="VIEW" if x["table_type"] == "VIEW" else "MANAGED",
                isTemporary=False,
            )
            for x in results
        ]
        for table in self.session.temp_views.keys():
            tables.append(
                Table(
                    name=table,  # type: ignore
                    catalog=None,
                    namespace=[],
                    description=None,
                    tableType="VIEW",
                    isTemporary=True,
                )
            )
        if pattern:
            tables = [
                x
                for x in tables
                if fnmatch.fnmatch(
                    x.name,
                    normalize_string(
                        pattern, from_dialect="input", to_dialect="output", is_pattern=True
                    ),
                )
            ]
        return tables


class ListColumnsFromInfoSchemaMixin(_BaseInfoSchemaMixin, t.Generic[SESSION, DF]):
    def listColumns(
        self, tableName: str, dbName: t.Optional[str] = None, include_temp: bool = False
    ) -> t.List[Column]:
        """Returns a t.List of columns for the given table/view in the specified database.

        .. versionadded:: 2.0.0

        Parameters
        ----------
        tableName : str
            name of the table to t.List columns.

            .. versionchanged:: 3.4.0
               Allow ``tableName`` to be qualified with catalog name when ``dbName`` is None.

        dbName : str, t.Optional
            name of the database to find the table to t.List columns.

        Returns
        -------
        t.List
            A t.List of :class:`Column`.

        Notes
        -----
        The order of arguments here is different from that of its JVM counterpart
        because Python does not support method overloading.

        If no database is specified, the current database and catalog
        are used. This API includes all temporary views.

        Examples
        --------
        >>> _ = spark.sql("DROP TABLE IF EXISTS tbl1")
        >>> _ = spark.sql("CREATE TABLE tblA (name STRING, age INT) USING parquet")
        >>> spark.catalog.t.listColumns("tblA")
        [Column(name='name', description=None, dataType='string', nullable=True, ...
        >>> _ = spark.sql("DROP TABLE tblA")
        """
        tableName = normalize_string(tableName, from_dialect="input", is_table=True)
        dbName = normalize_string(dbName, from_dialect="input", is_schema=True) if dbName else None
        if df := self.session.temp_views.get(tableName):
            return [
                Column(
                    name=x,
                    description=None,
                    dataType="",
                    nullable=True,
                    isPartition=False,
                    isBucket=False,
                )
                for x in df.columns
            ]

        table = exp.to_table(tableName, dialect=self.session.input_dialect)
        schema = to_schema(dbName, dialect=self.session.input_dialect) if dbName else None
        if not table.db:
            if schema and schema.db:
                table.set("db", schema.args["db"])
            else:
                current_database = normalize_string(
                    self.currentDatabase(), from_dialect="output", to_dialect="input"
                )
                table.set(
                    "db",
                    exp.parse_identifier(current_database, dialect=self.session.input_dialect),
                )
        if not table.catalog:
            if schema and schema.catalog:
                table.set("catalog", schema.args["catalog"])
            else:
                current_catalog = normalize_string(
                    self.currentCatalog(), from_dialect="output", to_dialect="input"
                )
                table.set(
                    "catalog",
                    exp.parse_identifier(current_catalog, dialect=self.session.input_dialect),
                )
        source_table = self._get_info_schema_table("columns", database=table.db)
        select = (
            exp.select(
                'column_name AS "column_name"',
                'data_type AS "data_type"',
                'is_nullable AS "is_nullable"',
            )
            .from_(source_table)
            .where(
                exp.column("table_name").eq(
                    normalize_string(
                        table.name,
                        from_dialect="input",
                        to_dialect="execution",
                        to_string_literal=True,
                    )
                )
            )
        )
        if table.db:
            schema_filter: exp.Expression = exp.column("table_schema").eq(
                normalize_string(
                    table.db, from_dialect="input", to_dialect="execution", to_string_literal=True
                )
            )
            if include_temp and self.TEMP_SCHEMA_FILTER:
                schema_filter = exp.Or(this=schema_filter, expression=self.TEMP_SCHEMA_FILTER)
            select = select.where(schema_filter)
        if table.catalog:
            catalog_filter: exp.Expression = exp.column("table_catalog").eq(
                normalize_string(
                    table.catalog,
                    from_dialect="input",
                    to_dialect="execution",
                    to_string_literal=True,
                )
            )
            if include_temp and self.TEMP_CATALOG_FILTER:
                catalog_filter = exp.Or(this=catalog_filter, expression=self.TEMP_CATALOG_FILTER)
            select = select.where(catalog_filter)
        results = self.session._fetch_rows(select)
        return [
            Column(
                name=normalize_string(
                    x["column_name"], from_dialect="execution", to_dialect="output"
                ),
                description=None,
                dataType=normalize_string(
                    x["data_type"], from_dialect="execution", to_dialect="output", is_datatype=True
                ),
                nullable=x["is_nullable"] == "YES",
                isPartition=False,
                isBucket=False,
            )
            for x in results
        ]
