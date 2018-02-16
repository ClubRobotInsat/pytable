class TableContext:
    """
    The metadata about the table currently opened in the editor.
    """

    def __init__(self, table):
        self.table = table

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table):
        self.__table = table
