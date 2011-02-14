# This file is part of f33dme.
#
#  f33dme is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  f33dme is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with f33dme.  If not, see <http://www.gnu.org/licenses/>.
#
# (C) 2011- by Adam Tauber, <asciimoo@gmail.com>

from django.db import models
from django.conf import settings
from datetime import datetime

class Tag(models.Model):
    text = models.CharField(max_length=64, unique=True)
    score = models.FloatField(default=0.0)

    def __unicode__(self):
        return '%s (%d/%d/X)' % (self.text, self.score, self.item_number())
   
    class Meta:
        ordering = ["-score"]
   
    class Admin:
        pass
    
    def item_number(self):
        return len(self.item_set.all())

    def get_link(self):
        return '<a href="/tags/%s">%s(%d)</a>' % (self.text, self.text, self.score)


class Feed(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=4096)
    tags = models.ManyToManyField(Tag)
    updated = models.DateTimeField(default=datetime(1970, 1, 1))
    score = models.FloatField(default=0.0)

    class Admin:
        pass
    
    def item_number(self):
        return len(self.item_set.all())

    def get_tags(self):
        return ', '.join([tag.get_link() for tag in self.tags.all()])
   


class Item(models.Model):
    title = models.CharField(max_length=4096)
    content = models.TextField()
    url = models.URLField()
    date = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    feed = models.ForeignKey(Feed)
    score = models.FloatField(default=0.0)
    archived = models.BooleanField(default=False)

   
    def __unicode__(self):
        if len(self.title) < 300:
            return self.title
        else:
            return self.title[:300] + " [...]"
   
    class Meta:
        ordering = ["-date"]
   
    class Admin:
        pass

    def get_tags(self):
        return ', '.join([tag.get_link() for tag in self.tags.all()])
   
    def get_nice_url(self):
        return ("%s/%d/%s") % (settings.ROOT_URL, self.id, self.title)
   