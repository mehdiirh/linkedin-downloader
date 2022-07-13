from mysql.connector import connect
from mysql.connector import errors

import settings

config = settings.DATABASE
config = {
    'user': config["USER"],
    'password': config["PASS"],
    'host': config["HOST"]
}


class Database:

    DB_NAME = 'linkedinDownloader'
    connection = None
    cursor = None

    def open(self):
        """
        Open database connection or create it if it doesn't exist

        Returns:
            (Database): self instance
        """

        for _ in range(3):
            try:
                self.connection = connect(
                    database=self.DB_NAME,
                    **config
                )
                return self
            except errors.ProgrammingError:
                self.create_db()

    def close(self):
        """
        Close database and cursor
        """

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_db(self):
        """
        Create database if it doesn't exist
        """

        database = connect(**config)
        cursor = database.cursor()
        cursor.execute(f"CREATE DATABASE {self.DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        cursor.close()
        database.close()

    def execute(self, operation: str, params: tuple = (), commit: bool = False):
        """
        Execute query

        Args:
            operation: SQL query
            params: SQL params
            commit (bool): set True to commit changes, False to ignore

        Returns:
            (bool): True
        """

        cursor = self.connection.cursor()
        cursor.execute(operation, params=params)
        if commit:
            self.connection.commit()
        cursor.close()
        return True

    def fetch(self, operation: str, size: int = None):
        """
        Fetch data from database

        Args:
            operation: SQL query
            size: item count to return

        Returns:
            (list): a list of result
        """

        cursor = self.connection.cursor(buffered=True)
        cursor.execute(operation)
        if size is not None:
            result = cursor.fetchmany(size)
        else:
            result = cursor.fetchall()

        if size == 1 and result:
            result = result[0]

        cursor.close()
        return result

    @staticmethod
    def create_filters(condition='AND', **filters):
        """
        Create filters from dict

        Args:
            condition: fill between filters with this phrase
            **filters: filters

        Returns:
            (str): SQL filters
        """

        _filters = []
        for key, value in filters.items():

            if value is None:
                value = 'NULL'

            if isinstance(value, (list, tuple)):
                value = list(map(lambda x: 'NULL' if x is None else x, value))

            if str(key).endswith('__in'):
                key = str(key).replace('__in', '')
                value = tuple(value)
                _filters.append(f'{key} IN {value}')
                continue

            if str(key).endswith('__contains'):
                key = str(key).replace('__contains', '')
                _filters.append(f'{key} LIKE "%{value}%"')
                continue

            if value == 'NULL':
                _filters.append(f'{key}=NULL')
            else:
                _filters.append(f'{key}="{value}"')

        return f' {condition} '.join(_filters)


class Model:

    table_name: str = ""

    def __init__(self):
        self.database = Database().open()
        self._create_table()

    def _create_table(self):
        """
        Create table if it doesn't exist
        """
        raise NotImplementedError("_create_table method is not implemented")

    def create(self, **kwargs):
        """
        Create a new row for table

        Args:
            **kwargs: key,values to insert

        Returns:
            bool: True
        """

        if not kwargs:
            raise ValueError("specify keys and values")

        length = ', '.join(['%s'] * len(kwargs))
        keys = ', '.join(kwargs.keys())

        self.database.execute(
            f"INSERT INTO {self.table_name} "
            f"({keys}) VALUES "
            f"({length})",

            params=tuple(kwargs.values()),
            commit=True
        )

        return True

    def fetch(self, columns=None, condition='AND', size=None, **filters):
        """
        Fetch data from database by filters and columns

        Args:
            columns: columns to return
            condition: fill between filters with this phrase
            size: item count to return
            **filters: filters to filter by

        Returns:
            (list): a list of results
        """

        if columns is None:
            columns = '*'

        if isinstance(columns, (list, tuple)):
            columns = ', '.join(columns)

        filters = self.database.create_filters(condition, **filters)

        query = f"SELECT {columns} FROM {self.table_name}"
        if filters:
            query += f" WHERE {filters}"

        return self.database.fetch(query, size=size)

    def update(self, values: dict, filters: dict, filter_condition='AND'):
        """
        Update data in database

        Args:
            values: values to update
            filters: filters to filter by
            filter_condition: fill between filters with this phrase

        Returns:
            (bool): True
        """

        values = self.database.create_filters(condition=',', **values)
        filters = self.database.create_filters(condition=filter_condition, **filters)

        return self.database.execute(
            f"UPDATE {self.table_name} SET {values} WHERE {filters}",
            commit=True
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()
