# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT
import os

from dotenv import load_dotenv
from readabilipy import simple_json_from_html_string

from .article import Article

load_dotenv()


class ReadabilityExtractor:
    def extract_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            html_content=article.get("content") if os.getenv('MAX_CONTENT_LENGTH') is None else article.get('content')[
                                                                                                0:os.getenv(
                                                                                                    'MAX_CONTENT_LENGTH')],
        )
