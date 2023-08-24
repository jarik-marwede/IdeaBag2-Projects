#!/usr/bin/env python3
"""An RSS module that can parse and save to RSS files.

Title:
RSS Feed Creator

Description:
A program which can read in text from other sources
and put it in RSS or Atom news format for syndication.
"""
import datetime
import xml.etree.ElementTree as ET
from email.utils import format_datetime, parsedate_to_datetime
from typing import List


class RSSItem:
    """An RSS item."""

    def __init__(self,
                 title: str,
                 link: str | None = None,
                 description: str | None = None,
                 author: str | None = None,
                 category: str | None = None,
                 comments: str | None = None,
                 enclosure: dict | None = None,
                 guid: str | None = None,
                 pub_date: datetime.datetime | None = None,
                 source: str | None = None):
        self.title = title
        self.link = link
        self.description = description
        self.author = author
        self.category = category
        self.comments = comments
        self.enclosure = enclosure
        self.guid = guid
        self.pub_date = pub_date
        self.source = source


class RSSDocument:
    """An RSS Document."""

    def __init__(self,
                 channel_title: str,
                 channel_link: str,
                 channel_description: str,
                 items: List[RSSItem],
                 language: str | None = None,
                 copyright: str | None = None,
                 managing_editor: str | None = None,
                 web_master: str | None = None,
                 pub_date: datetime.datetime | None = None,
                 last_build_date: datetime.datetime | None = None,
                 category: str | None = None,
                 generator: str | None = None,
                 docs: str | None = None,
                 cloud: dict | None = None,
                 ttl: int | None = None,
                 image: dict | None = None,
                 rating: str | None = None,
                 text_input: dict | None = None,
                 skip_hours: list | None = None,
                 skip_days: list | None = None):
        self.channel_title = channel_title
        self.channel_link = channel_link
        self.channel_description = channel_description
        self.items = items
        self.language = language
        self.copyright = copyright
        self.managing_editor = managing_editor
        self.web_master = web_master
        self.pub_date = pub_date
        self.last_build_date = last_build_date
        self.category = category
        self.generator = generator
        self.docs = docs
        self.cloud = cloud
        self.ttl = ttl
        self.image = image
        self.rating = rating
        self.text_input = text_input
        self.skip_hours = skip_hours
        self.skip_days = skip_days


class RSSFile:
    """An RSS file."""

    def __init__(self, file_name: str, rss_document: RSSDocument | None = None):
        self.file_name = file_name
        self.rss_document = rss_document

    def load(self):
        """Load the rss document from the file."""
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        channel = root.find("channel")

        channel_title = channel.find("title").text
        channel_link = channel.find("link").text
        channel_description = channel.find("description").text

        items = []
        for item in channel.findall("item"):
            item_title = item.find("title").text
            item_link_element = item.find("link")
            if item_link_element is not None:
                item_link = item_link_element.text
            else:
                item_link = None
            item_description_element = item.find("description")
            if item_description_element is not None:
                item_description = item_description_element.text
            else:
                item_description = None
            item_author_element = item.find("author")
            if item_author_element is not None:
                item_author = item_author_element.text
            else:
                item_author = None
            item_category_element = item.find("category")
            if item_category_element is not None:
                item_category = item_category_element.text
            else:
                item_category = None
            item_comments_element = item.find("comments")
            if item_comments_element is not None:
                item_comments = item_comments_element.text
            else:
                item_comments = None
            item_enclosure_element = item.find("enclosure")
            if item_enclosure_element is not None:
                item_enclosure = item_enclosure_element.attrib
            else:
                item_enclosure = None
            item_guid_element = item.find("guid")
            if item_guid_element is not None:
                item_guid = item_guid_element.text
            else:
                item_guid = None
            item_pub_date_element = item.find("pubDate")
            if item_pub_date_element is not None:
                item_pub_date = parsedate_to_datetime(item_pub_date_element.text)
            else:
                item_pub_date = None
            item_source_element = item.find("source")
            if item_source_element is not None:
                item_source = item_source_element.text
            else:
                item_source = None
            items.append(RSSItem(
                item_title,
                item_link,
                item_description,
                item_author,
                item_category,
                item_comments,
                item_enclosure,
                item_guid,
                item_pub_date,
                item_source
            ))

        language_element = channel.find("language")
        if language_element is not None:
            language = language_element.text
        else:
            language = None
        copyright_element = channel.find("copyright")
        if copyright_element is not None:
            copyright = copyright_element.text
        else:
            copyright = None
        managing_editor_element = channel.find("managingEditor")
        if managing_editor_element is not None:
            managing_editor = managing_editor_element.text
        else:
            managing_editor = None
        web_master_element = channel.find("webMaster")
        if web_master_element is not None:
            web_master = web_master_element.text
        else:
            web_master = None
        pub_date_element = channel.find("pubDate")
        if pub_date_element is not None:
            pub_date = parsedate_to_datetime(pub_date_element.text)
        else:
            pub_date = None
        last_build_date_element = channel.find("lastBuildDate")
        if last_build_date_element is not None:
            last_build_date = parsedate_to_datetime(last_build_date_element.text)
        else:
            last_build_date = None
        category_element = channel.find("category")
        if category_element is not None:
            category = category_element.text
        else:
            category = None
        generator_element = channel.find("generator")
        if generator_element is not None:
            generator = generator_element.text
        else:
            generator = None
        docs_element = channel.find("docs")
        if docs_element is not None:
            docs = docs_element.text
        else:
            docs = None
        cloud_element = channel.find("cloud")
        if cloud_element is not None:
            cloud = cloud_element.attrib
        else:
            cloud = None
        ttl_element = channel.find("ttl")
        if ttl_element is not None:
            ttl = int(ttl_element.text)
        else:
            ttl = None
        image_element = channel.find("image")
        if image_element is not None:
            image = {
                "url": image_element.find("url").text,
                "title": image_element.find("title").text,
                "link": image_element.find("link").text
            }
            if image_element.find("width") is not None:
                image["width"] = int(image_element.find("width").text)
            if image_element.find("height") is not None:
                image["height"] = int(image_element.find("height").text)
            if image_element.find("description") is not None:
                image["description"] = image_element.find("description").text
        else:
            image = None
        rating_element = channel.find("rating")
        if rating_element is not None:
            rating = rating_element.text
        else:
            rating = None
        text_input_element = channel.find("textInput")
        if text_input_element is not None:
            text_input = {
                "title": text_input_element.find("title").text,
                "description": text_input_element.find("description").text,
                "name": text_input_element.find("name").text,
                "link": text_input_element.find("link").text
            }
        else:
            text_input = None
        skip_hours_element = channel.find("skipHours")
        if skip_hours_element is not None:
            skip_hours = []
            for hour in skip_hours_element.find_all("hour"):
                skip_hours.append(int(hour.text))
        else:
            skip_hours = None
        skip_days_element = channel.find("skipDays")
        if skip_days_element is not None:
            skip_days = []
            for day in skip_days_element.find_all("day"):
                skip_days.append(day.text)
        else:
            skip_days = None

        self.rss_document = RSSDocument(
            channel_title,
            channel_link,
            channel_description,
            items,
            language,
            copyright,
            managing_editor,
            web_master,
            pub_date,
            last_build_date,
            category,
            generator,
            docs,
            cloud,
            ttl,
            image,
            rating,
            text_input,
            skip_hours,
            skip_days
        )

    def save(self):
        """Save the rss document to the file."""
        if not self.rss_document or not isinstance(self.rss_document, RSSDocument):
            raise TypeError(f"rss_document should be of type RSSDocument "
                            f"instead of type: {type(self.rss_document)}")
        tree = ET.ElementTree(ET.Element("rss", {"version": "2.0"}))
        root = tree.getroot()
        channel = ET.SubElement(root, "channel")
        channel_title = ET.SubElement(channel, "title")
        channel_title.text = self.rss_document.channel_title
        channel_link = ET.SubElement(channel, "link")
        channel_link.text = self.rss_document.channel_link
        channel_description = ET.SubElement(channel, "description")
        channel_description.text = self.rss_document.channel_description
        for item in self.rss_document.items:
            item_element = ET.SubElement(channel, "item")
            title = ET.SubElement(item_element, "title")
            title.text = item.title
            if item.link:
                link = ET.SubElement(item_element, "link")
                link.text = item.link
            if item.description:
                description = ET.SubElement(item_element, "description")
                description.text = item.description
            if item.author:
                author = ET.SubElement(item_element, "author")
                author.text = item.author
            if item.category:
                category = ET.SubElement(item_element, "category")
                category.text = item.category
            if item.comments:
                comments = ET.SubElement(item_element, "comments")
                comments.text = item.comments
            if item.enclosure:
                enclosure = ET.SubElement(item_element, "enclosure")
                enclosure.atrrib = item.enclosure
            if item.guid:
                guid = ET.SubElement(item_element, "guid")
                guid.text = item.guid
            if item.pub_date:
                pub_date = ET.SubElement(item_element, "pubDate")
                pub_date.text = format_datetime(item.pub_date)
            if item.source:
                source = ET.SubElement(item_element, "source")
                source.text = item.source
        if self.rss_document.language:
            language = ET.SubElement(channel, "language")
            language.text = self.rss_document.language
        if self.rss_document.copyright:
            copyright = ET.SubElement(channel, "copyright")
            copyright.text = self.rss_document.copyright
        if self.rss_document.managing_editor:
            managing_editor = ET.SubElement(channel, "managingEditor")
            managing_editor.text = self.rss_document.managing_editor
        if self.rss_document.web_master:
            web_master = ET.SubElement(channel, "webMaster")
            web_master.text = self.rss_document.web_master
        if self.rss_document.pub_date:
            pub_date = ET.SubElement(channel, "pubDate")
            pub_date.text = format_datetime(self.rss_document.pub_date)
        if self.rss_document.last_build_date:
            last_build_date = ET.SubElement(channel, "lastBuildDate")
            last_build_date.text = format_datetime(self.rss_document.last_build_date)
        if self.rss_document.category:
            category = ET.SubElement(channel, "category")
            category.text = self.rss_document.category
        if self.rss_document.generator:
            generator = ET.SubElement(channel, "generator")
            generator.text = self.rss_document.generator
        if self.rss_document.docs:
            docs = ET.SubElement(channel, "docs")
            docs.text = self.rss_document.docs
        if self.rss_document.cloud:
            cloud = ET.SubElement(channel, "cloud")
            cloud.attrib = self.rss_document.cloud
        if self.rss_document.ttl:
            ttl = ET.SubElement(channel, "ttl")
            ttl.text = self.rss_document.ttl
        if self.rss_document.image:
            image = ET.SubElement(channel, "image")
            ET.SubElement(image, "url").text = self.rss_document.image["url"]
            ET.SubElement(image, "title").text = self.rss_document.image["title"]
            ET.SubElement(image, "link").text = self.rss_document.image["link"]
            if "width" in self.rss_document.image:
                ET.SubElement(image, "width").text = self.rss_document.image["width"]
            if "height" in self.rss_document.image:
                ET.SubElement(image, "height").text = self.rss_document.image["height"]
            if "description" in self.rss_document.image:
                ET.SubElement(image, "description").text = self.rss_document.image["description"]
        if self.rss_document.rating:
            rating = ET.SubElement(channel, "rating")
            rating.text = self.rss_document.rating
        if self.rss_document.text_input:
            text_input = ET.SubElement(channel, "textInput")
            ET.SubElement(text_input, "title").text = self.rss_document.text_input["title"]
            ET.SubElement(text_input, "description").text = \
                self.rss_document.text_input["description"]
            ET.SubElement(text_input, "name").text = self.rss_document.text_input["name"]
            ET.SubElement(text_input, "link").text = self.rss_document.text_input["link"]
        if self.rss_document.skip_hours:
            skip_hours = ET.SubElement(channel, "skipHours")
            for hour in self.rss_document.skip_hours:
                ET.SubElement(skip_hours, "hour").text = hour
        if self.rss_document.skip_days:
            skip_days = ET.SubElement(channel, "skipDays")
            for day in self.rss_document.skip_days:
                ET.SubElement(skip_days, "hour").text = day

        tree.write(self.file_name)
