import sys
from datetime import datetime

from django.db import models
from mezzanine.pages.models import Page, RichText
from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager

# The members of Page will be inherited by the Author model, such
# as title, slug, etc. For authors we can use the title field to
# store the author's name. For our model definition, we just add
# any extra fields that aren't part of the Page model, in this
# case, date of birth.

class Profile(models.Model):
    type = ArrayField(dbtype="varchar(31)")
    follower_count = models.IntegerField()
    # groups INTEGER[]
    created  = models.DateTimeField() # should not have time zone
    last_active  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        last_active = datetime.now()
        return super(Profile, self).save(*args, **kwargs)

class ProfileOrganization(models.Model):
    profile_id = models.ForeignKey(Profile)
    name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    active = models.BooleanField()
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone
    website = models.CharField(max_length=255)
    size = models.CharField(max_length=63)
    alt_names = ArrayField(dbtype="varchar(255)")
    email_domains = ArrayField(dbtype="varchar(255)")

    class Meta:
        db_table="profile_organization"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileOrganization, self).save(*args, **kwargs)

    
class InviteCampaign(models.Model):
    owner_id = models.ForeignKey(ProfileOrganization, blank=True)
    name     = models.CharField(max_length=255)
    #follows  = ArrayField(dbtype="integer")
    #alt_names = ArrayField(dbtype="varchar(255)")
    #segments = models.  INTEGER[]
    #memberships = models.  INTEGER[]
    #roles    = models character varying[]
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone
    type     = models.CharField(max_length=60)
    active   = models.BooleanField()
    linkable = models.BooleanField()

    class Meta:
        db_table="invite_campaign"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteCampaign, self).save(*args, **kwargs)

class InviteBatch(models.Model):
    campaign_id = models.ForeignKey(InviteCampaign)
    # groups INTEGER[]
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="invite_batch"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteBatch, self).save(*args, **kwargs)


class InviteBatchRecipient(models.Model):
    member_id = models.ForeignKey(Profile,blank=True, null=True)
    batch_id  = models.ForeignKey(InviteBatch)
    email = models.CharField(max_length=255)
    key = models.CharField(max_length=1024)
    expired = models.BooleanField(default=False)
    name = models.CharField(max_length=127)
    used = models.BooleanField(default=False)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="invite_batch_recipient"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteBatchRecipient, self).save(*args, **kwargs)



class ProfileMember(models.Model):
    profile_id = models.ForeignKey(Profile)
    identity_id = models.IntegerField() # this seems like a key to something?
    email = models.CharField(max_length=255)
    key = models.CharField(max_length=1024)
    expired = models.BooleanField(default=False)
    name = models.CharField(max_length=127)
    batch_id = models.IntegerField()
    used = models.BooleanField(default=False)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile_member"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileMember, self).save(*args, **kwargs)

class ProfileSubCommunity(models.Model):
    profile_id = models.ForeignKey(Profile)
    name = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=127)
    parent_id = models.ForeignKey(Profile,related_name="profile_sub_community_parent")
    description = models.TextField() 
    image = models.CharField(max_length=255)
    active = models.BooleanField()
    private = models.BooleanField()
    email_domains = ArrayField(dbtype="varchar(64)")
    website = models.CharField(max_length=255)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile_sub_community"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileSubCommunity, self).save(*args, **kwargs)
