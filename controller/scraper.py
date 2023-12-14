# -*- encoding: utf-8 -*-
"""Models for the database of the pdok-crawler.

Copyright (C) 2017  Max Maass

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import os
import time
import magic
import requests
import subprocess
from multiprocessing.pool import ThreadPool, Process
from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, IntegerField, BooleanField, DateTimeField, ForeignKeyField, DoesNotExist

db = SqliteDatabase('pdoc.sqlite', threadlocals=True)


class Wahlperiode(Model):
    dbid = PrimaryKeyField()
    period_no = CharField(index=True)
    plenary_max = IntegerField(default=0)
    drucksache_max = IntegerField(default=0)
    period_scraped = BooleanField(default=False)
    period_uploaded = BooleanField(default=False)

    class Meta:
        database = db


class Document(Model):
    dbid = PrimaryKeyField()
    docno = CharField(index=True)
    archive_ident = CharField(null=True)
    title = CharField()
    date = DateTimeField()
    path = CharField()
    source = CharField()

    class Meta:
        database = db


class Drucksache(Document):
    doctype = CharField()
    urheber = CharField(null=True)
    autor = CharField(null=True)
    period = ForeignKeyField(Wahlperiode, related_name='drucksachen')


class Plenarprotokoll(Document):
    period = ForeignKeyField(Wahlperiode, related_name='plenarprotokolle')


def setup():
    db.connect()
    db.create_tables([Wahlperiode, Document, Drucksache, Plenarprotokoll], safe=True)

setup()


# Utility functions for downloading files, ...

# ... (The rest of the code remains unchanged)
