# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, User
from basic.utils import ErrHandle

# Create your models here.

LONG_STRING=255

# Models

# please view legend.txt document

class Information(models.Model):
    """Specific information that needs to be kept in the database"""

    # [1] The key under which this piece of information resides
    name = models.CharField("Key name", max_length=255)
    # [0-1] The value for this piece of information
    kvalue = models.TextField("Key value", default = "", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Information Items"

    def __str__(self):
        return self.name

    def get_kvalue(name):
        info = Information.objects.filter(name=name).first()
        if info == None:
            return ''
        else:
            return info.kvalue

    def set_kvalue(name, value):
        info = Information.objects.filter(name=name).first()
        if info == None:
            info = Information(name=name)
            info.save()
        info.kvalue = value
        info.save()
        return True

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        return super(Information, self).save(force_insert, force_update, using, update_fields)


class Emperor(models.Model):
    """The emperors that are portrayed by the portraits"""
    # [1] The names of the emperors
    name = models.CharField("Emperor", max_length=LONG_STRING)
    
    def __str__(self):
        return self.name

    def get_emperor_markdown(self):
        sBack = "-"
        if self.name:
            sBack = '<span class="emperor">{}</span>'.format(self.name)
        return sBack

class Context(models.Model):
    """The contexts (spaces or buildings) in which portraits were found"""
    # [1] The names of the contexts
    name = models.CharField("Context", max_length=LONG_STRING, blank=True, null=True)

    def __str__(self):
        return self.name

class Province(models.Model):
    """The names of Roman provinces in which the locations lie where the portraits have been found"""

    # CHANGE: here the location id, not in Location, this way location Unknown can handle an empty and a named province field
    # [1] Names of Roman province 
    name = models.CharField("Province", max_length=LONG_STRING, blank=True, null=True) # Is dat laatste nodig

    def __str__(self):
        return self.name

class Location(models.Model): 
    """Table that stores the locations where portraits have been found"""
    # Name of the place
    name = models.CharField("Place", max_length=LONG_STRING, blank = True, null = True)
    # Longitude of the place 
    long_coord = models.FloatField("Longitude coordinate",  blank = True, null = True)
    # Lattitude of the place
    lat_coord = models.FloatField("Lattitude coordinate",  blank = True, null = True)
    # The province where the portrait has been found
    province = models.ForeignKey(Province, null=True, blank=True, on_delete = models.CASCADE, related_name="location_province")

    def __str__(self):
        return self.name

class Portrait(models.Model):
    """The Portrait table is the core of the database, all other tables are linked (in)directly to this table"""

    # [1] Name of the portrait
    name = models.CharField("Name", max_length=LONG_STRING)    
    # [1] Original id of the portrat STRING
    origstr = models.CharField("Original ID", max_length=LONG_STRING, null=True, blank=True)
    # [0-1] References of the portrait # TH: maybe different via Zotero?
    reference = models.TextField("Reference", max_length=LONG_STRING, null=True, blank=True)
    # [1] Start date of the portrait
    startdate = models.IntegerField("Start date", null=True) 
    # [1] End date of the portrait
    enddate = models.IntegerField("End date", null=True)
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
    location = models.ForeignKey(Location, null=True, blank=True, on_delete = models.CASCADE, related_name="portrait_location")

    # [0-1] The id of the emperor that is portrayed
    emperor = models.ForeignKey(Emperor, null=True, blank=True, on_delete = models.CASCADE, related_name="portrait_emperor")
    
    # [0-1] The id of the emperor that is portrayed
    context = models.ForeignKey(Context, null=True, blank=True, on_delete = models.CASCADE, related_name="portrait_context")
 
    
    # Boolean characteristics for each portrait: zie legend.txt

    # [1] Whether the portrait is ...
    part_group = models.BooleanField(default=False)
    # [1] Whether the portrait is ...OLD
    # colossal = models.BooleanField(default=False)
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
    recarvedboo = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    terminus_ante_quem = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    terminus_post_quem = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    part_statue_group = models.BooleanField(default=False)   # ERUIT, zie part_group 
    # [1] Whether the portrait is ...
    contabulata = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    sword_belt = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    paludamentum = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    miniature = models.BooleanField(default=False)
    # [1] Whether the portrait is ...
    disputed = models.BooleanField(default=False)

 # ============== MANYTOMANY connections for Portrait
 
    # [m] Many-to-many: one portrait can have multiple portrait types 
    type = models.ManyToManyField("Type", through="PortraitType")

    # [m] Many-to-many: one portrait can have multiple alternative names
    alternative = models.ManyToManyField("Alternative", through="PortraitAlternative")

    # [m] Many-to-many: one portrait can have multiple subtypes 
    subtype = models.ManyToManyField("Subtype", through="PortraitSubtype")

    # [m] Many-to-many: one portrait can be made of multiple materials
    material = models.ManyToManyField("Material", through="PortraitMaterial")       
    
    # [m] Many-to-many: one portrait can have multiple recarvings 
    recarved_from = models.ManyToManyField("Recarved", through="PortraitRecarved")

    # [m] Many-to-many: one portrait can have multiple attributes
    attribute = models.ManyToManyField("Attributes", through="PortraitAttributes")

    # [m] Many-to-many: one portrait can have multiple iconongrapy items on cuirass
    iconography = models.ManyToManyField("Iconography", through="PortraitIconography")

    # [m] Many-to-many: one portrait can have multiple other wreath or crown items
    wreathcrown = models.ManyToManyField("Wreathcrown", through="PortraitWreathcrown")

    # [m] Many-to-many: one portrait can be together with multiple together items
    together = models.ManyToManyField("Together", through="PortraitTogether")
    
    def __str__(self):
        return self.name    

    def get_alternatives(self):
        lHtml = []
        # Visit all alternative type items
        for alternative in self.alternative.all().order_by('name'):            
            lHtml.append(alternative.name)  

        sBack = ", ".join(lHtml)
        return sBack

    def get_arachne(self):
        lHtml = []
        # Visit all arachne items        
        for arachne in self.arachne_portrait.all().order_by('arachne'):    
            # Add to list, make string of the integer
            lHtml.append(str(arachne.arachne))          
        sBack = ", ".join(lHtml)
        return sBack

    def get_attributes(self):
        lHtml = []
        # Visit all attribute items
        for attribute in self.attribute.all().order_by('name'):            
            lHtml.append(attribute.name)  

        sBack = ", ".join(lHtml)
        return sBack

    def get_context(self):
        lHtml = []
        # First check if there is a context linked to the portrait 
        if self.context != None:
            # If there is one, pick the province up
            cntxt = self.context.name   
            # And add it to list, 
            lHtml.append(cntxt)          
            sBack = ", ".join(lHtml)
        else:
            # If there is no context linked to a portrait
            # this needs to be marked with a "-" in order to skip the "empty" field
            # later in the process 
            lHtml.append("-")
            sBack = "".join(lHtml) 
        return sBack
    
    def get_iconography(self):
        lHtml = []
        # Visit all iconography items
        for iconography in self.iconography.all().order_by('name'):            
            lHtml.append(iconography.name) 
        sBack = ", ".join(lHtml)
        return sBack

    def get_materials(self):
        lHtml = []
        # Visit all material items
        for material in self.material.all().order_by('name'):            
            lHtml.append(material.name)            
        sBack = ", ".join(lHtml)
        return sBack 

    def get_photofolder(self):
        lHtml = []
        # Visit all photo items  
        for path in self.path_portrait.all().order_by('folder'):    
            # Add folder number to the list, make string of the integer
            lHtml.append(str(path.folder))          
        sBack = ", ".join(lHtml)
        return sBack

    def get_photopath(self):
        lHtml = []
        # Visit all photo items (no tiffs)      
        for item in self.path_portrait.all().order_by('folder'):    
            # Add path to list
            lHtml.append("<img src='/{}' style='max-width: 300px; width: auto; height: auto;'/>".format(item.path))
  

        sBack = "\n".join(lHtml)
        return sBack
           
    def get_photographer(self):
        lHtml = []
        # Visit the first photo path
        path1 = self.path_portrait.first()
        
        # Only move forward if there is a path (and thus picture)
        if path1 != None:      
            # Get the id of the photographer:
            id_grapher = path1.photographer_id
            # Only move forward when there is photographer associated with the image
            if id_grapher != None:
                # ok dit gaat goed
                # Get the corresponding object in the Photographer table                      
                namefound = Photographer.objects.filter(id__iexact=id_grapher).first()               
                # Add the name of the Photographer to the list
                lHtml.append(namefound.name) 
                sBack = ", ".join(lHtml)
            else:
                # If there is no photogrpaher linked to a portrait 
                # this needs to be marked with a "-" in order to skip the "empty" field
                # later in the process
                lHtml.append("-")
                sBack = "".join(lHtml)
        return sBack

    def get_province(self):
        lHtml = []
        # First check if there is a province linked to the location 
        if self.location.province != None:
            # If there is one, pick the province up
            prov = self.location.province.name   
            # And add it to list, 
            lHtml.append(prov)          
            sBack = ", ".join(lHtml)
        else:
            # If there is no province linked to a location
            # this needs to be marked with a "-" in order to skip the "empty" field
            # later in the process
            lHtml.append("-")
            sBack = "".join(lHtml)   
        return sBack    
    
    def get_recarvedstatue(self):
        lHtml = []
        oErr = ErrHandle()
        sBack = ""
        try:
            # Visit all recarved statues: 
            for recarved in self.recarved_from.all().order_by('name'):            
                lHtml.append(recarved.name)  
            sBack = ", ".join(lHtml)
        except:
            msg = oErr.get_error_message()
            oErr.DoError("get_carved")
        return sBack
    
    def get_subtypes(self):
        lHtml = []
        # Visit all subtype items
        for subtype in self.subtype.all().order_by('name'):            
            lHtml.append(subtype.name)  
        sBack = ", ".join(lHtml)
        return sBack

    def get_together(self):
        lHtml = []
        # Visit all together items
        for together in self.together.all().order_by('name'):            
            lHtml.append(together.name)  
        sBack = ", ".join(lHtml)
        return sBack
    
    def get_types(self):
        lHtml = []
        # Visit all type items
        for type in self.type.all().order_by('name'):            
            lHtml.append(type.name)  

        sBack = ", ".join(lHtml)
        return sBack  

    def get_wreathcrown(self):
        lHtml = []
        # Visit all wreath and crown items
        for wreathcrown in self.wreathcrown.all().order_by('name'):            
            lHtml.append(wreathcrown.name)  
        sBack = ", ".join(lHtml)
        return sBack    
  
class Arachne(models.Model):
    """The arachne code(s) that belong to a portrait"""
    # [0-1] The Arachne id 
    arachne = models.IntegerField("Arachne number")    
    # The id of the portrait that belongs to the Arachne code
    portrait = models.ForeignKey(Portrait, null=True, blank=True, on_delete = models.CASCADE, related_name="arachne_portrait")

    def __str__(self):
        return self.arachne

class Attributes(models.Model):
    """The attributes of a portrait"""
     # [1] The names of the attributes (type of attire, statuary type or figurative elements of the figure)
    name = models.CharField("Additional attributes", max_length=LONG_STRING, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Together(models.Model):
    """The objects that were originally displayed together with the portrait in the same environment"""
    # [1] The names of the objects
    name = models.CharField("Together with", max_length=LONG_STRING, blank=True, null=True)

    def __str__(self):
        return self.name
      
class Material(models.Model):
    """The substances of which the portrait has been made (if available)"""
    # [1] The names of the substances
    name = models.CharField("Material", max_length=LONG_STRING)

    def __str__(self):
        return self.name
    
class Type(models.Model):
    """The categories of portraits that the object belongs to based on the repetition of certain key features"""
    # [1] The names of the categories
    name = models.CharField("Type", max_length=LONG_STRING)

    def __str__(self):
        return self.name

class Alternative(models.Model):
    """The other names commonly used by authors to refer to the type of the portrait """
    # [1] The names of the alternative types
    name = models.CharField("Alternative type", max_length=LONG_STRING)

    def __str__(self):
        return self.name

class Subtype(models.Model):
    """The subcategories of portraits that the object belongs to based on the repetition of certain key features"""
    # [1] The names of the subcategories
    name = models.CharField("Subtype", max_length=LONG_STRING)

    def __str__(self):
        return self.name

class Wreathcrown(models.Model):
    """Other types of wreath or crown carried by the portrait that are not a corona laurea, civica or radiata"""
    # [1] Names of other wreath of crown of the portrait
    name =  models.CharField("Other wreath or crown", max_length=LONG_STRING, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Iconography(models.Model):
    """The descriptions of figurative decorations displayed on the breastplate"""
    # [1] The names of the decorations
    name = models.CharField("Iconography cuirass", max_length=LONG_STRING, blank=True, null=True)

    def __str__(self):
        return self.name

class Recarved(models.Model):
    """The former identity/identities of the portrait""" 
    # [1] The names of the identities
    name = models.CharField("Recarved portrait", max_length=LONG_STRING, blank=True, null=True)

    def __str__(self):
        return self.name

class Photographer(models.Model):
    """Some paths/photos have a link to a photographer"""
    # [1] The names of the photographers
    name = models.CharField("Name photographer", max_length=LONG_STRING, blank=True, null=True)

    def __str__(self):
        return self.name

class Path(models.Model):
    """One or paths (to photos) that are be linked to a portrait""" 
    # VIEW ARACHNE
    # [0-1] The path      
    path = models.CharField("Path name", max_length=LONG_STRING)
    # The id of the portrait that belongs to the Arachne code
    portrait = models.ForeignKey(Portrait, null=True, blank=True, on_delete = models.CASCADE, related_name="path_portrait")
    # [1] Filename of the folder with the photo's
    folder = models.IntegerField("Folder name", null=True) 
    # [0-1] The id of the photographer that made the photo (at the end of the path) ERUIT!
    photographer = models.ForeignKey(Photographer, null=True, blank=True, on_delete = models.CASCADE, related_name="path_photographer")
    
    def __str__(self):
        return self.path

# Add class PathPhotographer(models.Model):
    # [1] The portrait item
    # path = models.ForeignKey(Path, on_delete = models.CASCADE, related_name= "path_photographer")
    # [1] The together item
    # photographer = models.ForeignKey(Photographer, on_delete = models.CASCADE, related_name = "path_photographer")

       
# Here are the tables that link two tables with eachother

class PortraitTogether(models.Model): 
    """The link between a portrait and a together item"""

    # [1] The portrait item
    portrait = models.ForeignKey(Portrait, on_delete = models.CASCADE, related_name= "portrait_together")
    # [1] The together item
    together = models.ForeignKey(Together, on_delete = models.CASCADE, related_name = "portrait_together")

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