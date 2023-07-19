import logging
from aiogram import Bot, Dispatcher
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')
# storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')

# activate filters

dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
