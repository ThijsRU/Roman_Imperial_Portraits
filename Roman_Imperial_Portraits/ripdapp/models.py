# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

LONG_STRING=255

# Models

# please view legend.txt document

class Province(models.Model):
    """The names of Roman provinces in which the locations lie where the portraits have been found"""
    # [1] Names of Roman province 
    name = models.CharField("Province", max_length=LONG_STRING, blank=True, null=True)

class Location(models.Model): 
    """Table that stores the locations where portraits have been found"""
    # Name of the place
    name = models.CharField("Place", max_length=LONG_STRING, blank = True, null = True)
    # Longitude of the place 
    long_coord = models.FloatField("Longitude coordinate",  blank = True, null = True)
    # Lattitude of the place
    lat_coord = models.FloatField("Lattitude coordinate",  blank = True, null = True)
    # The province where the portrait has been found
    province = models.ForeignKey(Province, null=True, blank=True, on_delete = models.SET_NULL, related_name="location_province")



class Portrait(models.Model):
    """The Portrait table is the core of the database, all other tables are linked (in)directly to this table"""

    # [1] Name of the portrait
    name = models.CharField("Name", max_length=LONG_STRING)
    # [0-1] References of the portrait # TH: maybe different via Zotero?
    reference = models.TextField("Reference", max_length=LONG_STRING, null=True, blank=True)
    # [1] Start date of the portrait
    startdate = models.IntegerField("Start date", null=True) 
    # [1] End date of the portrait
    enddate = models.IntegerField("End date", null=True)
    # [0-1] Arachne number of the portrait,
    arachne = models.IntegerField("Arachne number", blank=True, null=True) 
    # [0-1] LSA number of the portrait
    lsa = models.IntegerField("LSA number", blank=True, null=True)
    # [0-1] The height of each portrait
    height = models.FloatField("Height", blank=True, null=True) 
    # [0-1] The comment on the height of each portrait
    height_comment = models.CharField("Comment_height", max_length=LONG_STRING, blank=True, null=True)       
    # [0-1] The name of the group of each portrait
    group_name = models.CharField("Name group", max_length=LONG_STRING, blank=True, null=True)
    # [0-1] The reference of the group of each portrait
    group_reference = models.TextField("Reference statue group", blank=True, null=True)       
    # [0-1] The reason for dating of each portrait
    reason_date = models.TextField("Reason dating", blank=True, null=True)

    # [0-1] The id of the location where the portrait was found
    location = models.ForeignKey(Location, null=True, blank=True, on_delete = models.SET_NULL, related_name="portrait_location")

    # Boolean characteristics for each portrait: zie legend.txt

    # [1] Whether the portrait is ...
    part_group = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    colossal = models.BooleanField(default=False)
    # [1] Whether the portrait has ...
    beard = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    buste = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    cuirassed_buste = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    capite_velato = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    headgear = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    corona_laurea = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    corona_civica = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    corona_radiata = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    other_wreath_crown = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    statue = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    toga = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    equestrian = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    cuirass = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    heroic_semi_nude = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    seated = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    recurved = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    terminus_ante_quem = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    terminus_post_quem = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    part_statue_group = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    relief = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    contabulata = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    sword_belt = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    paludamentum = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    miniature = models.BooleanField(default=False)

 # ============== MANYTOMANY connections for Portrait
 
    # [m] Many-to-many: one portrait can have multiple portrait types 
    type = models.ManyToManyField("Type", through="PortraitType")

    # [m] Many-to-many: one portrait can have multiple alternative names
    alternative = models.ManyToManyField("Alternative", through="PortraitAlternative")

    # [m] Many-to-many: one portrait can have multiple subtypes 
    subtype = models.ManyToManyField("Subtype", through="PortraitSubtype")

    # [m] Many-to-many: one portrait can be made of multiple materials
    material = models.ManyToManyField("Material", through="PortraitMaterial")       

    # [m] Many-to-many: one portrait can have multiple contexts ??
    context = models.ManyToManyField("Context", through="PortraitContext")

    # [m] Many-to-many: one portrait can have multiple recarvings 
    recarved = models.ManyToManyField("Recarved", through="PortraitRecarved")

    # [m] Many-to-many: one portrait can have multiple attributes
    attribute = models.ManyToManyField("Attributes", through="PortraitAttributes")

    # [m] Many-to-many: one portrait can have multiple iconongrapy items on cuirass
    iconography = models.ManyToManyField("Iconography", through="PortraitIconography")

    # [m] Many-to-many: one portrait can have multiple other wreath or crown items
    wreathcrown = models.ManyToManyField("Wreathcrown", through="PortraitWreathcrown")

    # [m] Many-to-many: one portrait can be together with multiple other portraits
    together = models.ManyToManyField("Together", through="PortraitTogether")

    def __str__(self):
        return self.name

# Here are the tables with FK's to Portrait

class Attributes(models.Model):
    """The attributes of a portrait"""
     # [1] The names of the attributes (type of attire, statuary type or figurative elements of the figure)
    name = models.CharField("Additional attributes", max_length=LONG_STRING, blank=True, null=True)

class Together(models.Model):
    """The objects that were originally displayed together with the portrait in the same environment"""
    # [1] The names of the objects
    name = models.CharField("Together with", max_length=LONG_STRING, blank=True, null=True)
  
class Material(models.Model):
    """The substances of which the portrait has been made (if available)"""
    # [1] The names of the substances
    name = models.CharField("Material", max_length=LONG_STRING)

class Emperor(models.Model):
    """The emperors that are portrayed by the portraits"""
    # [1] The names of the emperors
    name = models.CharField("Emperor", max_length=LONG_STRING)

class Type(models.Model):
    """The categories of portraits that the object belongs to based on the repetition of certain key features"""
    # [1] The names of the categories
    name = models.CharField("Type", max_length=LONG_STRING)

class Alternative(models.Model):
    """The other names commonly used by authors to refer to the type of the portrait """
    # [1] The names of the alternative types
    name = models.CharField("Alternative type", max_length=LONG_STRING)

class Subtype(models.Model):
    """The subcategories of portraits that the object belongs to based on the repetition of certain key features"""
    # [1] The names of the subcategories
    name = models.CharField("Subtype", max_length=LONG_STRING)

class Wreathcrown(models.Model):
    """Other types of wreath or crown carried by the portrait that are not a corona laurea, civica or radiata"""
    # [1] Names of other wreath of crown of the portrait
    name =  models.CharField("Other wreath or crown", max_length=LONG_STRING, blank=True, null=True)

class Iconography(models.Model):
    """The descriptions of figurative decorations displayed on the breastplate"""
    # [1] The names of the decorations
    name = models.CharField("Iconography cuirass", max_length=LONG_STRING, blank=True, null=True)

class Context(models.Model):
    """The contexts (spaces or buildings) in which portraits can be found"""
    # [1] The names of the contexts
    name = models.CharField("Context", max_length=LONG_STRING, blank=True, null=True)
    
class Recarved(models.Model):
    """The former identity/identities of the portrait""" 
    # [1] The names of the identities
    name = models.CharField("Recarved portrait", max_length=LONG_STRING, blank=True, null=True)

class Photographer(models.Model):
    """Some photos have a link to a photographer"""
    # [1] The names of the photographers
    name = models.CharField("Name photographer", max_length=LONG_STRING, blank=True, null=True)

class Photo(models.Model):
    """One or photos that are be linked to a portrait"""
    
    # [1] Filename of the photo
    filename = models.CharField("Filename", max_length=LONG_STRING, blank=True, null=True)
    # [1] Link/path to the photo TH: how will this work?
    hyperlink = models.CharField("Link?", max_length=LONG_STRING, blank=True, null=True)# ? intern? Dit is ooit extern bedoeld?
    # [1] Order of importance of each photo linked to a specific portraits
    order = models.IntegerField("Order of photos", blank=True, null=True) 
    # [1] The portrait to which the photo belongs 
    portrait = models.ForeignKey(Portrait, null=True, blank=True, on_delete = models.SET_NULL, related_name="portrait_photo")
    # [0-1] The id of the photographer that made the photo
    photographer = models.ForeignKey(Photographer, null=True, blank=True, on_delete = models.SET_NULL, related_name="photo_photographer")
    
# Here are the tables that link two tables with eachother

class PortraitTogether(models.Model): 
    """The link between a portrait and a together item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name= "portrait_together")
    # [1] The together item
    together = models.ForeignKey(Together, on_delete = models.CASCADE, related_name = "portrait_together")

class PortraitEmperor(models.Model): 
    """The link between a portrait and emperor item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_emperor")
    # [1] The emperor that is portrayed by the portrait
    emperor = models.ForeignKey(Emperor, on_delete = models.CASCADE, related_name = "portrait_emperor")

class PortraitType(models.Model):
    """The link between a portrait and a portrait type"""
    
    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_type")
    # [1] The portrait type (or types) 
    type = models.ForeignKey(Type,on_delete = models.CASCADE, related_name = "portrait_type")

class PortraitAlternative(models.Model):
    """The link between a portrait and one or more alternative name items"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_alternative")
    # [1] The alternative name or names of a portrait type
    alternative = models.ForeignKey(Alternative, on_delete = models.CASCADE,related_name = "portrait_alternative")
    
class PortraitSubtype(models.Model):
    """The link between a portrait and one or more sub type items"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait,on_delete = models.CASCADE, related_name="portrait_subtype")
    # [1] The subtype of a portrait
    subtype = models.ForeignKey(Subtype,on_delete = models.CASCADE, related_name = "portrait_subtype")
    
class PortraitMaterial(models.Model):
    """The link between a portrait and material item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_material")
    # [1] The material or materials of which a portrait is made from
    material = models.ForeignKey(Material, on_delete = models.CASCADE,related_name = "portrait_material")

class PortraitContext(models.Model):
    """The link between a portrait and the context item"""
    
    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_context")
    # [1] The context in which the portrait is found
    context = models.ForeignKey(Context, on_delete = models.CASCADE, related_name = "portrait_context")
    
class PortraitRecarved(models.Model):
    """The link between a portrait and a recarved item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_recarved")
    # [1] The recarved item or items related to the portrait
    recarved = models.ForeignKey(Recarved, on_delete = models.CASCADE, related_name = "portrait_recarved")

class PortraitAttributes(models.Model):
    """The link between a portrait and an attribute item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_attributes")
    # [1] The attribute item or items related to the portrait
    attribute = models.ForeignKey(Attributes, on_delete = models.CASCADE, related_name = "portrait_attributes")

class PortraitIconography(models.Model):
    """The link between a portrait and an iconography on cuirass item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_iconography")
    # [m] The cuirass iconography item or items related to the portrait
    iconography = models.ForeignKey(Iconography, on_delete = models.CASCADE, related_name = "portrait_iconography")

class PortraitWreathcrown(models.Model):
    """The link between a portrait and a wreath or crown item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name="portrait_wreathcrown")
    # [m] The wreathe or crown item or items related to the portrait
    wreathcrown = models.ForeignKey(Wreathcrown, on_delete = models.CASCADE, related_name = "portrait_wreathcrown")