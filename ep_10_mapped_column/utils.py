from typing import Optional

from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

str_20 = Annotated[str, mapped_column(String(20))]
str_50 = Annotated[str, mapped_column(String(50))]
str_70 = Annotated[String(70), mapped_column()]
str_100 = Annotated[Optional[str], mapped_column(String(100))]

int_small = Annotated[SmallInteger, mapped_column(SmallInteger)]
int_big = Annotated[BigInteger, mapped_column(BigInteger)]

# Default Type Map:
#
# type_map: Dict[Type[Any], TypeEngine[Any]] = {
#     bool: types.Boolean(),
#     bytes: types.LargeBinary(),
#     datetime.date: types.Date(),
#     datetime.datetime: types.DateTime(),
#     datetime.time: types.Time(),
#     datetime.timedelta: types.Interval(),
#     decimal.Decimal: types.Numeric(),
#     float: types.Float(),
#     int: types.Integer(),
#     str: types.String(),
#     uuid.UUID: types.Uuid(),
# }
