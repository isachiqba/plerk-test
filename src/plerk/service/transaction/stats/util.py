import decimal
import logging
import pygments
import pygments.formatters.terminal256
import pygments.lexers
import sqlparse


class PrettySQL(logging.Formatter):

  FORMATTER = pygments.formatters.terminal256.TerminalTrueColorFormatter(style="monokai")
  LEXER = pygments.lexers.get_lexer_by_name("sql")

  def format(self, record):
    prettysql = record.sql.strip()
    prettysql = sqlparse.format(prettysql, keyword_case="upper", reindent_aligned=True)
    prettysql = pygments.highlight(prettysql, self.LEXER, self.FORMATTER)
    record.prettysql = prettysql
    return super(PrettySQL, self).format(record)


def fmt_cents_to_basic_unit(cents: int, *, exp=decimal.Decimal("0.01")):
  value = decimal.Decimal(cents)
  value = value / 100
  value = value.quantize(exp)
  value = str(value)
  return value
