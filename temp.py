from mailing_bot.shp_mailing_bot.notion_parse.notion_parser import NotionParser

Parser = NotionParser(693767247)
Parser.read_database()
Parser._find_field_meaning()

