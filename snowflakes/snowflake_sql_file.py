from IPython.core.magic import (Magics, register_line_magic, magics_class, line_magic,
                                cell_magic, line_cell_magic, needs_local_scope)

try:
    from traitlets.config.configurable import Configurable
except ImportError:
    from IPython.config.configurable import Configurable

import snowflake.connector
from pandas import DataFrame
from snowflake.connector import DictCursor

# The class MUST call this class decorator at creation time
@magics_class
class Snowflake_Sql(Magics, Configurable):

    def __init__(self, shell):
        Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)

        # Add ourself to the list of module configurable via %config
        self.shell.configurables.append(self)
        self.connection, self.engine = None, None
        self.username, self.password, self.account = None, None, None
    
   
    @needs_local_scope
    @line_magic('snowflakes')
    @cell_magic('snowflakes')
    def execute(self, line, cell='', local_ns={}):        
        if not self.username:
            line.strip()
            self.username, self.password, self.account = line.split(" ")
            self.connection = snowflake.connector.connect(
              user=self.username,
              password=self.password,
              account=self.account,
            )

        if len(cell) > 0:
            try:
                cursor = self.connection.cursor(DictCursor)
                results = []               
                for cmd in cell.split(";")[:-1]:
                    result = cursor.execute(cmd).fetchall()
                    results.append(result)                
                self.shell.user_ns.update({line: DataFrame(results[-1])})
            finally:
                try:
                    cursor.close()
                except Exception as e:
                    return e
            return DataFrame(results[-1])
        else:
            return None
        
    def __del__(self):
        self.connection.close()