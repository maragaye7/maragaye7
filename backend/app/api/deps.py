from typing import Annotated

from fastapi import Depends

from app.dolibarr import DolibarrClient, get_dolibarr_client

DolibarrDep = Annotated[DolibarrClient, Depends(get_dolibarr_client)]
