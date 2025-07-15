import logging

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  handlers=[
    logging.StreamHandler()
  ]
)

logger = logging.getLogger(__name__)
logging.getLogger('discord').setLevel(logging.WARNING)

# Channel
LOG_MESSAGE_EDIT = your_channel_id