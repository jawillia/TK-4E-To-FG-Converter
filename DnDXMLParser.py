import xml.etree.ElementTree as ET
import sys
import re as regularExpression

class RacialTrait():
	def __init__(self, internal_id, traitName, race, shortdescription):
		self.internal_id = internal_id
		self.traitName = traitName
		self.race = race
		self.shortdescription = shortdescription
		self.fullDescription = ""

class ClassFeature():
	def __init__(self, featureName, shortdescription, level):
		self.featureName = featureName
		self.shortdescription = shortdescription
		self.level = level
		self.fullDescription = ""

class Feat():
	def __init__(self, featName, prerequisites, featDescription, tier, special, type, shortdescription, associatedPowerInfo, associatedPowers):
		self.featName = featName
		self.prerequisites = prerequisites
		self.featDescription = featDescription
		self.tier = tier
		self.special = special
		self.type = type
		self.shortdescription = shortdescription
		self.associatedPowerInfo = associatedPowerInfo
		self.associatedPowers = associatedPowers
		self.fullDescription = ""

class InventoryItem():
	def __init__(self, itemName, count, carried, showonminisheet, weight):
		self.itemName = itemName
		self.count = count
		self.carried = carried
		self.location = ""
		self.showonminisheet = showonminisheet
		self.weight = weight
		self.itemClass = ""
		self.damage = ""
		self.flavor = ""
		self.itemGroup = ""
		self.isIdentified = None
		self.isLocked = None
		self.mitype = None
		self.proficiencyBonus = None
		self.properties = None
		self.subclass = None
		self.range = None
		self.fgmitype = ""
		self.cost = ""
		self.level = 0
		self.rarity = ""
		self.magicItemType = ""

class Power():
	def __init__(self, powerName, action, keywords, prepared, powerRange, recharge, shortdescription, source):
		self.powerName = powerName
		self.action = action
		self.keywords = keywords
		self.prepared = prepared
		self.powerRange = powerRange
		self.recharge = recharge
		self.shortdescription = shortdescription
		self.source = source

class Skill():
	def __init__(self, skillName, skillMiscBonus, skillAbility, abilityBonus, totalBonus, trained, hasArmorPenalty, armorPenalty):
		self.skillName = skillName
		self.skillMiscBonus = skillMiscBonus
		self.skillAbility = skillAbility
		self.abilityBonus = abilityBonus
		self.totalBonus = totalBonus
		self.trained = trained
		self.hasArmorPenalty = hasArmorPenalty
		self.armorPenalty = armorPenalty

class Character():
	def __init__(self, characterName=None, className=None, level=None, levelBonus=None, player=None, height=None, weight=None,
		gender=None,age=None,alignment=None,company=None,portrait=None,experience=None,experienceNeeded=None,carriedMoney=None,
		storedMoney=None,traits=None,appearance=None,companions=None,notes=None,strength=None,dexterity=None,constitution=None,
		wisdom=None,intelligence=None,charisma=None,strengthModifier=None,dexterityModifier=None,constitutionModifier=None,
		wisdomModifier=None,intelligenceModifier=None,charismaModifier=None):
		self.characterName = characterName
		self.className = className
		self.level = level
		self.levelBonus = levelBonus
		self.player = player
		self.height = height
		self.weight = weight
		self.gender = gender
		self.age = age
		self.alignment = alignment
		self.company = company
		self.portrait = portrait
		self.experience = experience
		self.experienceNeeded = experienceNeeded
		self.carriedMoney = carriedMoney
		self.storedMoney = storedMoney
		self.traits = traits
		self.appearance = appearance
		self.companions = companions
		self.notes = notes
		self.strength = strength
		self.dexterity = dexterity
		self.constitution = constitution
		self.wisdom = wisdom
		self.intelligence = intelligence
		self.charisma = charisma
		self.strengthModifier = strengthModifier
		self.dexterityModifier = dexterityModifier
		self.constitutionModifier = constitutionModifier
		self.wisdomModifier = wisdomModifier
		self.intelligenceModifier = intelligenceModifier
		self.charismaModifier = charismaModifier
		self.isHeavyArmorEquipped = False
		self.isLightArmorEquipped = False
		self.defenseAC = 0
		self.armor = 0
		self.armorCheckPenalty = 0
		self.armorSpeedPenalty = 0
		self.defenseFortitude = 0
		self.defenceReflex = 0
		self.defenceWill = 0
		self.deity = ""
		self.currentCarriedWeight = 0
		self.maxHp = 0
		self.maxSurges = 0
		self.initiative = 0
		self.initiativeMiscBonus = 0
		self.race = ""
		self.size = ""
		self.baseSpeed = 0
		self.totalSpeed = 0
		self.featsListRulesElements = []
		self.languageRulesElements = []
		self.armorProficiencyElements = []
		self.weaponProficiencyElements = []
		self.inventoryList = []
		self.powerList = []
		self.skillList = []
		self.featList = []
		self.classFeatureList = []
		self.racialTraitList = []

	def appendInventory(self, value):
		self.inventoryList.append(value)

	def appendPower(self, value):
		self.powerList.append(value)

	def appendSkill(self, value):
		self.skillList.append(value)

	def appendFeat(self, value):
		self.featList.append(value)

	def appendClassFeature(self, value):
		self.classFeatureList.append(value)

	def appendRacialTrait(self, value):
		self.racialTraitList.append(value)


#Reading from .dnd4e file
def readCBLoaderCharacterFile(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	charactersheetSection = root[0]

	#Character Sheet Sections
	detailSection = charactersheetSection[0]
	statBlocksSection = charactersheetSection[2]
	rulesElementTallySection = charactersheetSection[3]
	lootTallySection = charactersheetSection[4]
	powersStatsSection = charactersheetSection[5]

	#Other Top Level Sections
	levelSection = root[2]
	levelRulesOneElementSection = levelSection[0]

	character = Character(detailSection.find(".//name").text.strip())

	#Reading Character Sheet > Details
	character.characterName = detailSection.find(".//name").text.strip()
	character.level = detailSection.find(".//Level").text.strip()
	character.levelBonus = int(character.level)//2
	character.player = detailSection.find(".//Player").text.strip()
	character.height = detailSection.find(".//Height").text.strip()
	character.weight = detailSection.find(".//Weight").text.strip()
	#This doesn't work. Have to get the gender from a different section
	#character.gender = detailSection.find(".//Gender").text.strip()
	character.age = detailSection.find(".//Age").text.strip()
	#This doesn't work. Have to get the alignnment from a different section.
	#character.alignment = detailSection.find(".//Alignment").text.strip()
	character.comapany = detailSection.find(".//Company").text.strip()
	character.portrait = detailSection.find(".//Portrait").text.strip()
	character.experience = detailSection.find(".//Experience").text.strip()
	character.carriedMoney = detailSection.find(".//CarriedMoney").text.strip()
	character.storedMoney = detailSection.find(".//StoredMoney").text.strip()
	character.traits = detailSection.find(".//Traits").text.strip()
	character.appearance = detailSection.find(".//Appearance").text.strip()
	character.companions = detailSection.find(".//Companions").text.strip()
	character.notes = detailSection.find(".//Notes").text.strip()

	#Class
	classElement = rulesElementTallySection.find(".//RulesElement[@type='Class']")
	if classElement is not None:
		character.className = classElement.get("name")

	#Reading Ability Scores
	for stat in statBlocksSection.findall("Stat"):
	    alias = stat.find("alias")
	    if alias is not None and alias.get("name") == "Strength":
	        character.strength = stat.get("value")
	        character.strengthModifier = (int(character.strength)-10)//2
	        print("Str score:", character.strength)
	    elif alias is not None and alias.get("name") == "Constitution":
	        character.constitution = stat.get("value")
	        character.constitutionModifier = (int(character.constitution)-10)//2
	        print("Con score:", character.constitution)
	    elif alias is not None and alias.get("name") == "Dexterity":
	        character.dexterity = stat.get("value")
	        character.dexterityModifier = (int(character.dexterity)-10)//2
	        print("Dex score:",character.dexterity)
	    elif alias is not None and alias.get("name") == "Intelligence":
	        character.intelligence = stat.get("value")
	        character.intelligenceModifier = (int(character.intelligence)-10)//2
	        print("Int score:", character.intelligence)
	    elif alias is not None and alias.get("name") == "Wisdom":
	        character.wisdom = stat.get("value")
	        character.wisdomModifier = (int(character.wisdom)-10)//2
	        print("Wis score:", character.wisdom)
	    elif alias is not None and alias.get("name") == "Charisma":
	        character.charisma = stat.get("value")
	        character.charismaModifier = (int(character.charisma)-10)//2
	        print("Cha score:", character.charisma)

	#Read Defenses
	#Determine Light or Heavy Armor because it determines some defense stats
	for loot in lootTallySection.findall(".//loot[@equip-count='1']"):
		rulesElement = loot.find(".//RulesElement[@type='Armor']")
		if rulesElement is not None:
			equippedArmor = rulesElement.get("name")
			match equippedArmor:
				case "Cloth Armor":
					character.isLightArmorEquipped = True
				case "Leather Armor":
					character.isLightArmorEquipped = True
				case "Hide Armor":
					character.isLightArmorEquipped = True
				case "Chainmail":
					character.isHeavyArmorEquipped = True
				case "Scale Armor":
					character.isHeavyArmorEquipped = True
				case "Plate Armor":
					character.isHeavyArmorEquipped = True

	#AC/Fort/Ref/Will
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "AC":                   #AC
			character.defenseAC = stat.get("value")
			armorElement = stat.find(".//statadd[@type='Armor']")
			if armorElement is not None and armorElement.get("value") is not None:
				character.armor = armorElement.get("value")
		elif alias is not None and alias.get("name") == "Fortitude Defense":           #Fortitude
			character.defenseFortitude = stat.get("value")
		elif alias is not None and alias.get("name") == "Reflex Defense":              #Reflex
			character.defenseReflex = stat.get("value")
		elif alias is not None and alias.get("name") == "Will Defense":                #Will
			character.defenseWill = stat.get("value")

	#Deity
	deityElement = rulesElementTallySection.find(".//RulesElement[@type='Deity']")
	if deityElement is not None:
		character.deity = deityElement.get("name")

	#Encumberance Stats
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "Armor Penalty":
			character.armorCheckPenalty = stat.get("value")
		if alias is not None and alias.get("name") == "Weight":
			character.currentCarriedWeight = stat.get("value")

	#Experience Needed
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "XP Needed":
			character.experienceNeeded = stat.get("value")

	#Feats
	character.featsListRulesElements = rulesElementTallySection.findall(".//RulesElement[@type='Feat']")

	#Gender
	genderRulesElement = rulesElementTallySection.find(".//RulesElement[@type='Gender']")
	if genderRulesElement is not None:
		character.gender = genderRulesElement.get("name");

	#Alignment
	alignmentElement = rulesElementTallySection.find(".//RulesElement[@type='Alignment']")
	if alignmentElement is not None:
		character.alignment = alignmentElement.get("name")		

	#HP
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "Hit Points":	
			character.maxHp = stat.get("value")
		elif alias is not None and alias.get("name") == "Healing Surges":
			character.maxSurges = stat.get("value")

	#Initiative
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "Initiative":
			character.initiative = stat.get("value")
		elif alias is not None and alias.get("name") == "Initiative Misc":
			character.initiativeMiscBonus = stat.get("value")

	#Inventory List
	for inventoryElement in lootTallySection:
		itemName = inventoryElement[0].get("name")
		count = inventoryElement.get("count")
		carried = "1" if inventoryElement.get("count") != "0" else "0"
		showonminisheet = 1
		weight = 0
		inventoryitem = InventoryItem(itemName, count, carried, showonminisheet, weight)
		character.appendInventory(inventoryitem)

	#Languages
	character.languageRulesElements = rulesElementTallySection.findall(".//RulesElement[@type='Language']")

	#Powers
	for powerElement in powersStatsSection.findall("Power"):
		powerName = powerElement.get("name")
		powerActionTypeElement = powerElement.find(".//specific[@name='Action Type']")
		if powerActionTypeElement is not None:
			powerAction = powerActionTypeElement.text.strip()
		powerPrepared = "1"
		powerUsageElement = powerElement.find(".//specific[@name='Power Usage']")
		if powerUsageElement is not None:
			powerRecharge = powerUsageElement.text.strip()
		power = Power(powerName, powerAction, "", powerPrepared, "", powerRecharge, "", "")
		character.appendPower(power)

	#Armor Proficiencies
	character.armorProficiencyElements = []
	for armorProficiencyElementRead in rulesElementTallySection.findall(".//RulesElement[@type='Proficiency']"):
		if "Armor Proficiency" in armorProficiencyElementRead.get("name"):
			character.armorProficiencyElements.append(armorProficiencyElementRead)

	#Weapon Proficiencies
	character.weaponProficiencyElements = []
	for weaponProficiencyElementRead in rulesElementTallySection.findall(".//RulesElement[@type='Proficiency']"):
		if "Weapon Proficiency" in weaponProficiencyElementRead.get("name"):
			character.weaponProficiencyElements.append(weaponProficiencyElementRead)

	#Race
	raceElement = rulesElementTallySection.find(".//RulesElement[@type='Race']")
	if raceElement is not None:
		character.race = raceElement.get("name")
	#Size
	sizeElement = rulesElementTallySection.find(".//RulesElement[@type='Size']")
	if sizeElement is not None:
		character.size = sizeElement.get("name")

	#Skills
	levelRulesOneSkillRulesElementSection = levelRulesOneElementSection[0]
	for skillRulesSection in levelRulesOneSkillRulesElementSection.findall(".//RulesElement[@type='Skill']"):
		skillName = skillRulesSection.get("name")
		for stat in statBlocksSection.findall("Stat"):
			alias = stat.find("alias")
			if alias is not None and alias.get("name") == skillRulesSection.get("name"):
				totalBonus = stat.get("value")
				skillAbility = stat.find(".//statadd[@type='Ability']").get("statlink") if stat.find(".//statadd[@type='Ability']") is not None else "" 
				isArmorPenalty = stat.find(".//statadd[@type='Armor Penalty']").get("value") if stat.find(".//statadd[@type='Armor Penalty']") is not None else 0
				armorPenalty = 0
				trained = "0"
				skillMiscBonus = 0
				abilityModifier = eval("character." + skillAbility.lower() + "Modifier")
				if isArmorPenalty == "1":
					for statArmorPenalty in statBlocksSection.findall("Stat"):
						armorPenaltyAlias = statArmorPenalty.find("alias")
						if armorPenaltyAlias is not None and armorPenaltyAlias.get("name") == "Armor Penalty":
							armorPenalty = statArmorPenalty.get("value")
				for statTrained in statBlocksSection.findall("Stat"):
					trainedStatAlias = statTrained.find("alias")
					if trainedStatAlias is not None and trainedStatAlias.get("name") == skillName + " Trained":
						trainedBonus = statTrained.get("value")
						if int(trainedBonus) > 0 : trained = "1"
				for statMisc in statBlocksSection.findall("Stat"):
					miscStatAlias = statMisc.find("alias")
					if miscStatAlias is not None and miscStatAlias.get("name") == skillName + " Misc":
						skillMiscBonus = int(statMisc.get("value"))
		skill = Skill(skillName, skillMiscBonus, skillAbility, abilityModifier, totalBonus, trained, isArmorPenalty, armorPenalty)
		character.appendSkill(skill)

	#Special Abilities
	#Class Features
	classFeatureElementSection = rulesElementTallySection.findall(".//RulesElement[@type='Class Feature']")
	for classFeatureElement in classFeatureElementSection:
		classFeatureName = classFeatureElement.get("name")
		classFeatureShortDescription = ""
		classFeatureShortDescriptionElement = classFeatureElement.find(".//specific[@name='Short Description']")
		if classFeatureShortDescriptionElement is not None:
			classFeatureShortDescription = classFeatureShortDescriptionElement.text.strip() if classFeatureShortDescriptionElement.text is not None else ""
		classFeature = ClassFeature(classFeatureName, classFeatureShortDescription, "1")
		character.appendClassFeature(classFeature)
	#Racial Traits
	racialTraitElementSection = rulesElementTallySection.findall(".//RulesElement[@type='Racial Trait']")
	for racialTraitElement in racialTraitElementSection:
		racialTraitID = racialTraitElement.get("internal-id")
		racialTraitName = racialTraitElement.get("name")
		racialTraitShortDescription = ""
		racialTraitShortDescriptionElement = racialTraitElement.find(".//specific[@name='Short Description']")
		if racialTraitShortDescriptionElement is not None:
			racialTraitShortDescription = racialTraitShortDescriptionElement.text.strip() if racialTraitShortDescriptionElement.text is not None else ""
		racialTrait = RacialTrait(racialTraitID, racialTraitName, None, racialTraitShortDescription)
		character.appendRacialTrait(racialTrait)

	#Speed
	for stat in statBlocksSection.findall("Stat"):
		alias = stat.find("alias")
		if alias is not None and alias.get("name") == "Speed":
			character.armorSpeedPenalty = stat.find(".//statadd[@type='Armor']").get("value") if stat.find(".//statadd[@type='Armor']") is not None else "0"
			character.baseSpeed = stat.find(".//statadd[@Level='1']").get("value") if stat.find(".//statadd[@Level='1']") is not None else "0"
			character.totalSpeed = stat.get("value")

	return character



#Reading from the original character loader XML file and loads it into an existing character file
def readCBLoaderMainFile(character, mergedFileLocation = None):
	#These fields are in the main file and missing from the character-specific one
	if mergedFileLocation is None:
		mergedFileLocation = "static/characterBuilderLibraries/combined.dnd40.merged.xml"
	tree = ET.parse(mergedFileLocation)
	root = tree.getroot()

	#Feats
	for featElement in character.featsListRulesElements:
		featName = featElement.get("name")
		featRulesElement = root.find(".//RulesElement[@name=\""+ featName + "\"][@type='Feat']")
		if featRulesElement is not None:
			featDescription = ""
			featPrerequisites = ""
			featTier = ""
			featSpecial = ""
			featType = ""
			featShortDescription = ""
			featAssociatedPowerInfo = ""
			featAssociatedPowers = ""
			featFullDescription = ""
			#Tier
			featTierElement = featRulesElement.find(".//specific[@name='Tier']")
			if featTierElement is not None:
				featTier = featTierElement.text.strip() if featTierElement.text is not None else ""
				if featTierElement != "":
					featFullDescription = featFullDescription + "Tier: " + featTier + "\\n"			
			#Prerequisites
			featPrereqElement = featRulesElement.find(".//Prereqs")
			if featPrereqElement is not None:
				featPrerequisites = featPrereqElement.text.strip() if featPrereqElement.text is not None else ""
				if featPrerequisites != "":
					featFullDescription = featFullDescription + "Prerequisites: " + featPrerequisites + "\\n\\n"		
			#Type
			featTypeElement = featRulesElement.find(".//specific[@name='type']")
			if featTypeElement is not None:
				featType = featTypeElement.text.strip() if featTypeElement.text is not None else ""
				if featType != "":
					featFullDescription = featFullDescription + "Type: " + featType + "\\n\\n"
			#Short Description
			featShortDescriptionElement = featRulesElement.find(".//specific[@name='Short Description']")
			if featShortDescriptionElement is not None:
				featShortDescription = featShortDescriptionElement.text.strip() if featShortDescriptionElement.text is not None else ""			
			#Description
			featDescription = featRulesElement[-1].tail
			if featDescription != None and featDescription != "":
				featFullDescription = featFullDescription + "Benefit: " + featDescription + "\\n"				
			#Associated Power Info
			featAssociatedPowerElement = featRulesElement.find(".//specific[@name='Associated Power Info']")
			if featAssociatedPowerElement is not None:
				featAssociatedPowerInfo = featAssociatedPowerElement.text.strip() if featAssociatedPowerElement.text is not None else ""	
				if featAssociatedPowerInfo != "":
					featFullDescription = featFullDescription + "Associated Power Info: " + featAssociatedPowerInfo + "\\n\\n"
			#Associated Powers
			featAssociatedPowersElement = featRulesElement.find(".//specific[@name='Associated Powers']")
			if featAssociatedPowerElement is not None:
				featAssociatedPowers = featAssociatedPowersElement.text.strip() if featAssociatedPowersElement.text is not None else ""			
				if featAssociatedPowers != "":
					featFullDescription = featFullDescription + "Associated Powers: " + featAssociatedPowers + "\\n"
			#Special
			featSpecialElement = featRulesElement.find(".//specific[@name='Special']")
			if featSpecialElement is not None:
				featSpecial = featSpecialElement.text.strip() if featSpecialElement.text is not None else ""
				if featSpecial != "":
					featFullDescription = featFullDescription + "\\nSpecial: " + featSpecial + "\\n"
			#Put together into Feat and Add to Character
			feat = Feat(featName, featPrerequisites, featDescription, featTier, featSpecial, featType, featShortDescription, featAssociatedPowerInfo, featAssociatedPowers)
			feat.fullDescription = featFullDescription
			character.appendFeat(feat)


	#Inventory List
	for inventoryElement in character.inventoryList:
		itemName = inventoryElement.itemName
		itemRulesElement = root.find(".//RulesElement[@name=\""+ itemName +"\"]")
		if itemRulesElement is not None:
			itemWeight = ""
			itemSlot = ""
			itemClass = ""
			itemDamage = ""
			itemFlavor = ""
			itemGroup = ""
			itemMagicItemType = ""
			itemProficiencyBonus = ""
			itemProperties = ""
			itemSubclass = ""
			itemRange = ""
			itemFGMIType = ""
			itemCost = ""
			itemLevel = ""
			itemRarity = ""
			#Fantasy Grounds Item MIType
			if itemClass == "Weapon":
				itemFGMIType = "weapon"
			elif itemClass == "Armor":
				itemFGMIType = "armor"
			else:
				itemFGMIType = "other"			
			#Level
			itemLevelElement = itemRulesElement.find(".//specific[@name='Level']")
			if itemLevelElement is not None:
				itemLevel = itemLevelElement.text.strip() if itemLevelElement.text is not None else "0"
			#Weight
			itemWeightElement = itemRulesElement.find(".//specific[@name='Weight']")
			if itemWeightElement is not None:
				itemWeight = itemWeightElement.text.strip() if itemWeightElement.text is not None else "0"
			#Location
			itemSlotElement = itemRulesElement.find(".//specific[@name='Item Slot']")
			if itemSlotElement is not None:
				itemSlot = itemSlotElement.text.strip() if itemSlotElement.text is not None else ""
			#Item Class
			itemClass = itemRulesElement.get("type")
			if itemClass is not None:
				itemClass = itemClass.strip()
			#Damage
			itemDamageElement = itemRulesElement.find(".//specific[@name='Damage']")
			if itemDamageElement is not None:
				itemDamage = itemDamageElement.text.strip() if itemDamageElement.text is not None else ""
			#Flavor
			itemFlavorElement = itemRulesElement.find(".//Flavor")
			if itemFlavorElement is not None:
				itemFlavor = itemFlavorElement.text.strip() if itemFlavorElement.text is not None else ""
			else:
				last_child = itemRulesElement[-1]
				itemFlavor = last_child.tail.strip()
			#Item Group
			itemGroupElement = itemRulesElement.find(".//specific[@name='Group']")
			if itemGroupElement is not None:
				itemGroup = itemGroupElement.text.strip() if itemGroupElement.text is not None else ""
			#Magic Item Type
			itemMagicItemTypeElement = itemRulesElement.find(".//specific[@name='Magic Item Type']")
			if itemMagicItemTypeElement is not None:
				itemMagicItemType = itemMagicItemTypeElement.text.strip() if itemMagicItemTypeElement.text is not None else ""
			#ProficiencyBonus
			itemProfBonusElement = itemRulesElement.find(".//specific[@name='Proficiency Bonus']")
			if itemProfBonusElement is not None:
				itemProficiencyBonus = itemProfBonusElement.text.strip() if itemProfBonusElement.text is not None else ""
			#Properties
			itemPropertiesElement = itemRulesElement.find(".//specific[@name='Properties']")
			if itemPropertiesElement is not None:
				itemProperties = itemPropertiesElement.text.strip() if itemPropertiesElement.text is not None else ""
			#Subclass
			if itemClass == "Alternative Reward":
				itemSubclassElement = itemRulesElement.find(".//specific[@name='Alternative Reward']")
				if itemSubclassElement is not None:
					itemSubclass = itemSubclassElement.text.strip() if itemSubclassElement.text is not None else ""
			elif itemClass == "Gear":
				itemSubclassElement = itemRulesElement.find(".//specific[@name='Category']")
				if itemSubclassElement is not None:
					itemSubclass = itemSubclassElement.text.strip() if itemSubclassElement.text is not None else ""					
			elif itemClass == "Magic Item":
				itemSubclassElement = itemRulesElement.find(".//specific[@name='Item Slot']")
				if itemSubclassElement is not None:
					itemSubclass = itemSubclassElement.text.strip() if itemSubclassElement.text is not None else ""				
			elif itemClass == "Weapon":
				itemSubclassElement = itemRulesElement.find(".//specific[@name='Weapon Category']")
				if itemSubclassElement is not None:
					itemSubclass = itemSubclassElement.text.strip() if itemSubclassElement.text is not None else ""
			#Item Range
			itemRangeElement = itemRulesElement.find(".//specific[@name='Range']")
			if itemRangeElement is not None:
				itemRange = itemRangeElement.text.strip() if itemRangeElement.text is not None else ""
			#Item Rarity
			itemRarityElement = itemRulesElement.find(".//specific[@name='Rarity']")
			if itemRarityElement is not None:
				itemRarity = itemRarityElement.text.strip() if itemRarityElement.text is not None else ""
			#Item Cost
			goldCost = ""
			silverCost = ""
			copperCost = ""
			itemGoldCostElement = itemRulesElement.find(".//specific[@name='Gold']")
			if itemGoldCostElement is not None:
				goldCost = itemGoldCostElement.text.strip() + " gp" if itemGoldCostElement.text is not None else ""
			itemSilverCostElement = itemRulesElement.find(".//specific[@name='Silver']")
			if itemSilverCostElement is not None:
				silverCost = itemSilverCostElement.text.strip + " sp" if itemSilverCostElement.text is not None else ""
			itemCopperCostElement = itemRulesElement.find(".//specific[@name='Copper']")
			if itemCopperCostElement is not None:
				copperCost = itemCopperCostElement.text.strip + " cp" if itemCopperCostElement.text is not None else ""
			itemCost = goldCost + silverCost + copperCost	
			#Finish Adding Stats to the Items
			for inventoryItem in character.inventoryList:
				if inventoryItem.itemName == itemName:
					inventoryItem.weight = itemWeight
					inventoryItem.location = itemSlot
					inventoryItem.itemClass = itemClass
					inventoryItem.magicItemType = itemMagicItemType
					inventoryItem.itemDamage = itemDamage
					inventoryItem.flavor = itemFlavor
					inventoryItem.itemGroup = itemGroup
					inventoryItem.mitype = itemMagicItemType
					inventoryItem.proficiencyBonus = itemProficiencyBonus
					inventoryItem.properties = itemProperties
					inventoryItem.subclass = itemSubclass
					inventoryItem.range = itemRange
					inventoryItem.fgmitype = itemFGMIType
					inventoryItem.cost = itemCost
					inventoryItem.level = itemLevel
					inventoryItem.rarity = itemRarity

	#Powers
	for power in character.powerList:
		powerRulesElementList = root.findall(".//RulesElement[@name=\""+ power.powerName +"\"][@type='Power']")
		#Get the last item of the list since it seems to generally be the most recent one.
		#TODO:Should probably compare revision dates to make it correct, though
		powerRulesElement = powerRulesElementList[-1]
		powerKeywords = ""
		powerRange = ""
		powerDescription = ""
		powerSource = ""
		#Keywords
		keywordsRuleElement = powerRulesElement.find(".//specific[@name='Keywords']")
		if keywordsRuleElement is not None:
			powerKeywords = keywordsRuleElement.text.strip() if keywordsRuleElement.text is not None else ""
		#Range
		rangeRuleElement = powerRulesElement.find(".//specific[@name='Attack Type']")
		if rangeRuleElement is not None:
			powerRange = rangeRuleElement.text.strip() if rangeRuleElement.text is not None else ""
		#Short Description
		shortDescriptionRuleElements = powerRulesElement.findall(".//")
		for element in shortDescriptionRuleElements:
			if (("name" not in element.attrib and "Category" not in element.tag) or 
				("name" in element.attrib and element.attrib["name"] != "Power Usage" 
					and element.attrib["name"] != "Display" 
					and element.attrib["name"] != "Keywords"
					and element.attrib["name"] != "Action Type"
					and element.attrib["name"] != "Attack Type"
					and element.attrib["name"] != "Class"
					and element.attrib["name"] != "Level"
					and element.attrib["name"] != "Power Type"
					and element.attrib["name"] != "Powers"
					and "_" not in element.attrib["name"])):
				if "name" in element.attrib and powerDescription is not None and element.text is not None:
					powerDescription = powerDescription + str(element.attrib["name"]) + ": " + element.text + "\\n"
				elif powerDescription is not None and element.text is not None:
					powerDescription = powerDescription + element.text + "\\n\\n"
		#Source
		sourceRuleElement = powerRulesElement.find(".//specific[@name='Display']")
		if sourceRuleElement is not None:
			powerSource = sourceRuleElement.text.strip() if sourceRuleElement.text is not None else ""			
		#Finish Adding Stats to the Powers
		for characterPower in character.powerList:
			if characterPower.powerName == power.powerName:
				characterPower.keywords = powerKeywords
				characterPower.powerRange = powerRange
				characterPower.shortdescription = powerDescription
				characterPower.source = powerSource

	#Special Ability
	#Class Features
	for classFeature in character.classFeatureList:
		classFeatureRulesElement = root.find(".//RulesElement[@name=\""+ classFeature.featureName + "\"][@type='Class Feature']")
		if classFeatureRulesElement is not None:
			classFeatureFullDescription = ""
			#Description
			classFeatureFullDescription = classFeatureRulesElement[-1].tail
			if classFeatureFullDescription != None and classFeatureFullDescription != "":
				classFeature.fullDescription = classFeature.fullDescription + classFeatureFullDescription + "\\n\\n"	
			#Sub-Features
			classFeatureSubFeatureElement = classFeatureRulesElement.find(".//specific[@name='_PARSED_SUB_FEATURES']")
			if classFeatureSubFeatureElement != None and classFeatureSubFeatureElement != "":
				classFeatureSubFeatureText = classFeatureSubFeatureElement.text
				if classFeatureSubFeatureText != None:
					classFeatureSubFeatureList = classFeatureSubFeatureText.strip().split()
					for subFeatureID in classFeatureSubFeatureList:
						subFeatureRulesElement = root.find(".//RulesElement[@internal-id=\""+ subFeatureID.replace(',','') + "\"]")
						if subFeatureRulesElement != None:
							classFeature.fullDescription = classFeature.fullDescription + subFeatureRulesElement.attrib["name"] + "\\n"	
							subFeatureShortDescriptionElement = subFeatureRulesElement.find(".//specific[@name='Short Description']")
							if subFeatureShortDescriptionElement != None:
								subFeatureShortDescription = subFeatureShortDescriptionElement.text.strip() if subFeatureShortDescriptionElement.text is not None else ""
								if subFeatureShortDescription != None and subFeatureShortDescription != "":
									classFeature.fullDescription = classFeature.fullDescription + subFeatureShortDescription + "\\n\\n"	
	#Racial Traits
	for racialTrait in character.racialTraitList:
		racialTraitRulesElement = root.find(".//RulesElement[@name=\"" + racialTrait.traitName + "\"][@type='Racial Trait']")
		if racialTraitRulesElement is not None:
			racialTraitRace = ""
			racialTraitFullDescription = ""
			#Race
			#grantedRacialFeaturesElement = root.find(".//RulesElement[@internal-id=\"" + racialTrait.internal_id + "\"][@type='Grants']")
			#Description
			racialTraitFullDescription = racialTraitRulesElement[-1].tail
			if racialTraitFullDescription != None and racialTraitFullDescription != "":
				racialTrait.fullDescription = racialTrait.fullDescription + racialTraitFullDescription + "\\n\\n"
			#Sub-Features
			racialTraitSubFeatureElement = racialTraitRulesElement.find(".//specific[@name='_PARSED_SUB_FEATURES']")
			if racialTraitSubFeatureElement != None and racialTraitSubFeatureElement != "":
				racialTraitSubFeatureText = racialTraitSubFeatureElement.text
				if racialTraitSubFeatureText != None:
					racialTraitSubFeatureList = racialTraitSubFeatureText.strip().split()
					for subFeatureID in racialTraitSubFeatureList:
						subFeatureRulesElement = root.find(".//RulesElement[@internal-id=\""+ subFeatureID.replace(',','') + "\"]")
						if subFeatureRulesElement != None:
							racialTrait.fullDescription = racialTrait.fullDescription + subFeatureRulesElement.attrib["name"] + "\\n"	
							subFeatureShortDescriptionElement = subFeatureRulesElement.find(".//specific[@name='Short Description']")
							if subFeatureShortDescriptionElement != None:
								subFeatureShortDescription = subFeatureShortDescriptionElement.text.strip() if subFeatureShortDescriptionElement.text is not None else ""
								if subFeatureShortDescription != None and subFeatureShortDescription != "":
									racialTrait.fullDescription = racialTrait.fullDescription + subFeatureShortDescription + "\\n\\n"					
			

	return character;



#Writing To new XML File
def writeFantasyGroundsFile(character, outputFilename = None, outputType = None) -> None:
	if outputFilename is None:
		outputFilename = "output.xml"
	if outputType is None:
		outputType = "dataOnlyOption"
	rootWrite = ET.Element("root")
	rootWrite.set('version', '4.5')
	rootWrite.set('dataversion', '20230911')
	rootWrite.set('release', '28|CoreRPG:6')
	characterWrite = ET.SubElement(rootWrite, "character")

	#Writing Ability Scores
	abilitiesWrite = ET.SubElement(characterWrite, "abilities")
	#Charisma
	chaBonusWrite = ET.SubElement(abilitiesWrite, "charisma")
	ET.SubElement(chaBonusWrite, "bonus", type="number").text = str(character.charismaModifier)
	ET.SubElement(chaBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(chaBonusWrite, "check", type="number").text = str(character.charismaModifier)
	ET.SubElement(chaBonusWrite, "score", type="number").text = character.charisma
	#Constitution
	conBonusWrite = ET.SubElement(abilitiesWrite, "constitution")
	ET.SubElement(conBonusWrite, "bonus", type="number").text = str(character.constitutionModifier)
	ET.SubElement(conBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(conBonusWrite, "check", type="number").text = str(character.constitutionModifier)
	ET.SubElement(conBonusWrite, "score", type="number").text = character.constitution
	#Dexterity
	dexBonusWrite = ET.SubElement(abilitiesWrite, "dexterity")
	ET.SubElement(dexBonusWrite, "bonus", type="number").text = str(character.dexterityModifier)
	ET.SubElement(dexBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(dexBonusWrite, "check", type="number").text = str(character.dexterityModifier)
	ET.SubElement(dexBonusWrite, "score", type="number").text = character.dexterity
	#Intelligence
	intBonusWrite = ET.SubElement(abilitiesWrite, "intelligence")
	ET.SubElement(intBonusWrite, "bonus", type="number").text = str(character.intelligenceModifier)
	ET.SubElement(intBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(intBonusWrite, "check", type="number").text = str(character.intelligenceModifier)
	ET.SubElement(intBonusWrite, "score", type="number").text = character.intelligence
	#Strength
	strBonusWrite = ET.SubElement(abilitiesWrite, "strength")
	ET.SubElement(strBonusWrite, "bonus", type="number").text = str(character.strengthModifier)
	ET.SubElement(strBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(strBonusWrite, "check", type="number").text = str(character.strengthModifier)
	ET.SubElement(strBonusWrite, "score", type="number").text = character.strength
	#Wisdom
	wisBonusWrite = ET.SubElement(abilitiesWrite, "wisdom")
	ET.SubElement(wisBonusWrite, "bonus", type="number").text = str(character.wisdomModifier)
	ET.SubElement(wisBonusWrite, "bonusmodifier", type="number").text = "0"
	ET.SubElement(wisBonusWrite, "check", type="number").text = str(character.wisdomModifier)
	ET.SubElement(wisBonusWrite, "score", type="number").text = character.wisdom

	#Age
	ageWrite = ET.SubElement(characterWrite, "age", type="string").text = character.age

	#Alignment
	ET.SubElement(characterWrite, "alignment", type="string").text = character.alignment

	#Action Points Used (AP Used)
	apUsedWrite = ET.SubElement(characterWrite, "apused", type="number").text = "0"

	#Appearance
	appearanceWrite = ET.SubElement(characterWrite, "appearance", type="string").text = character.appearance

	#Attacks
	attacksWrite = ET.SubElement(characterWrite, "attacks")
	meleeAttacksWrite = ET.SubElement(attacksWrite, "melee")
	ET.SubElement(meleeAttacksWrite, "ability", type="number").text = str(character.strengthModifier)
	ET.SubElement(meleeAttacksWrite, "misc", type="number").text = "0"
	ET.SubElement(meleeAttacksWrite, "temporary", type="number").text = "0"
	ET.SubElement(meleeAttacksWrite, "total", type="number").text = str(character.strengthModifier)
	rangedAttacksWrite = ET.SubElement(attacksWrite, "ranged")
	ET.SubElement(rangedAttacksWrite, "ability", type="number").text = str(character.dexterityModifier)
	ET.SubElement(rangedAttacksWrite, "misc", type="number").text = "0"
	ET.SubElement(rangedAttacksWrite, "temporary", type="number").text = "0"
	ET.SubElement(rangedAttacksWrite, "total", type="number").text = str(character.dexterityModifier)

	#Charisma Check Modifier
	charismacheckmodifierWrite = ET.SubElement(characterWrite, "charismacheckmodifier", type="number").text = "0"

	#Class
	classWrite = ET.SubElement(characterWrite, "class")
	baseClassWrite = ET.SubElement(classWrite, "base", type="string").text = character.className

	#Coins
	moneyAD = 0
	moneyPP = 0
	moneyGP = 0
	moneySP = 0
	moneyCP = 0
	carriedMoneyList = character.carriedMoney.split("; ")
	for carriedMoney in carriedMoneyList:
		if "ad" in carriedMoney:
			moneyAD = carriedMoney.split()[0]
		elif "pp" in carriedMoney:
			moneyPP = carriedMoney.split()[0]
		elif "gp" in carriedMoney:
			moneyGP = carriedMoney.split()[0]
		elif "sp" in carriedMoney:
			moneySP = carriedMoney.split()[0]
		elif "cp" in carriedMoney:
			moneyCP = carriedMoney.split()[0]
	coinsWrite = ET.SubElement(characterWrite, "coin")
	coinsADWrite = ET.SubElement(coinsWrite, "id-00001")
	ET.SubElement(coinsADWrite, "amount", type="number").text = moneyAD
	ET.SubElement(coinsADWrite, "name", type="string").text = "AD"
	coinsResiduumWrite = ET.SubElement(coinsWrite, "id-00002")
	ET.SubElement(coinsResiduumWrite, "amount", type="number").text = "0"
	ET.SubElement(coinsResiduumWrite, "name", type="string").text = "RESIDUUM"
	coinsPPWrite = ET.SubElement(coinsWrite, "id-00003")
	ET.SubElement(coinsPPWrite, "amount", type="number").text = moneyPP
	ET.SubElement(coinsPPWrite, "name", type="string").text = "PP"
	coinsGPWrite = ET.SubElement(coinsWrite, "id-00004")
	ET.SubElement(coinsGPWrite, "amount", type="number").text = moneyGP
	ET.SubElement(coinsGPWrite, "name", type="string").text = "GP"
	coinsSPWrite = ET.SubElement(coinsWrite, "id-00005")
	ET.SubElement(coinsSPWrite, "amount", type="number").text = moneySP
	ET.SubElement(coinsSPWrite, "name", type="string").text = "SP"	
	coinsCPWrite = ET.SubElement(coinsWrite, "id-00006")
	ET.SubElement(coinsCPWrite, "amount", type="number").text = moneyCP
	ET.SubElement(coinsCPWrite, "name", type="string").text = "CP"

	#Constitution Check Modifier	
	constitutioncheckmodifierWrite = ET.SubElement(characterWrite, "constitutioncheckmodifier", type="number").text = "0"

	#Defenses
	defensesWrite = ET.SubElement(characterWrite, "defenses")
	#AC
	armorclassAbilityBonus = 0
	defensesACWrite = ET.SubElement(defensesWrite, "ac")
	if not character.isHeavyArmorEquipped and character.dexterityModifier >= character.intelligenceModifier:
		armorclassAbilityBonus = character.dexterityModifier
	elif not character.isHeavyArmorEquipped and character.intelligenceModifier > character.dexterityModifier:
		armorclassAbilityBonus = character.intelligenceModifier
	ET.SubElement(defensesACWrite, "ability", type="number").text = str(armorclassAbilityBonus)
	ET.SubElement(defensesACWrite, "armor", type="number").text = character.armor
	ET.SubElement(defensesACWrite, "base", type="number").text = "10"
	ET.SubElement(defensesACWrite, "misc", type="number").text = str(int(character.defenseAC) - (10 + armorclassAbilityBonus + int(character.armor)))
	ET.SubElement(defensesACWrite, "temporary", type="number").text = "0"
	ET.SubElement(defensesACWrite, "total", type="number").text = character.defenseAC
	#Fortitude
	fortitudeAbilityBonus = 0
	defensesFortWrite = ET.SubElement(defensesWrite, "fortitude")
	if character.strengthModifier >= character.constitutionModifier:
		fortitudeAbilityBonus = character.strengthModifier
	elif character.constitutionModifier > character.strengthModifier:
		fortitudeAbilityBonus = character.constitutionModifier
	ET.SubElement(defensesFortWrite, "ability", type="number").text = str(fortitudeAbilityBonus)
	ET.SubElement(defensesFortWrite, "base", type="number").text = "10"
	ET.SubElement(defensesFortWrite, "misc", type="number").text = str(int(character.defenseFortitude) - (10 + fortitudeAbilityBonus))
	ET.SubElement(defensesFortWrite, "temporary", type="number").text = "0"
	ET.SubElement(defensesFortWrite, "total", type="number").text = character.defenseFortitude
	#Reflex
	reflexAbilityBonus = 0
	defensesReflexWrite = ET.SubElement(defensesWrite, "reflex")
	if character.dexterityModifier >= character.intelligenceModifier:
		reflexAbilityBonus = character.dexterityModifier
	elif character.intelligenceModifier > character.dexterityModifier:
		reflexAbilityBonus = character.intelligenceModifier
	ET.SubElement(defensesReflexWrite, "ability", type="number").text = str(reflexAbilityBonus)
	ET.SubElement(defensesReflexWrite, "armor", type="number").text = "0"
	ET.SubElement(defensesReflexWrite, "base", type="number").text = "10"
	ET.SubElement(defensesReflexWrite, "misc", type="number").text = str(int(character.defenseReflex) - (10 + reflexAbilityBonus))
	ET.SubElement(defensesReflexWrite, "temporary", type="number").text = "0"
	ET.SubElement(defensesReflexWrite, "total", type="number").text = character.defenseReflex
	#Save
	defensesSaveWrite = ET.SubElement(defensesWrite, "save")
	ET.SubElement(defensesSaveWrite, "base", type="number").text = "0"
	ET.SubElement(defensesSaveWrite, "misc", type="number").text = "0"
	ET.SubElement(defensesSaveWrite, "temporary", type="number").text = "0"
	ET.SubElement(defensesSaveWrite, "total", type="number").text = "0"
	#Will
	willAbilityBonus = 0
	defensesWillWrite = ET.SubElement(defensesWrite, "will")
	if character.wisdomModifier >= character.charismaModifier:
		willAbilityBonus = character.wisdomModifier
	elif character.charismaModifier > character.wisdomModifier:
		willAbilityBonus = character.charismaModifier
	ET.SubElement(defensesWillWrite, "ability", type="number").text = str(willAbilityBonus)
	ET.SubElement(defensesWillWrite, "base", type="number").text = "10"
	ET.SubElement(defensesWillWrite, "misc", type="number").text = str(int(character.defenseWill) - (10 + willAbilityBonus))
	ET.SubElement(defensesWillWrite, "temporary", type="number").text = "0"
	ET.SubElement(defensesWillWrite, "total", type="number").text = character.defenseWill

	#Deity
	ET.SubElement(characterWrite, "deity", type="string").text = character.deity

	#Dexterity Check Modifier
	dexteritycheckmodifierWrite = ET.SubElement(characterWrite, "dexteritycheckmodifier", type="number").text = "0"

	#Encumberance
	encumberanceWrite = ET.SubElement(characterWrite, "encumberance")
	ET.SubElement(encumberanceWrite, "armorcheckpenalty", type="number").text = character.armorCheckPenalty
	ET.SubElement(encumberanceWrite, "dragload", type="number").text = str(int(character.strength)*50)
	ET.SubElement(encumberanceWrite, "heavyarmor", type="number").text = "1" if character.isHeavyArmorEquipped == True else "0"
	ET.SubElement(encumberanceWrite, "heavyload", type="number").text = str(int(character.strength)*20)
	ET.SubElement(encumberanceWrite, "load", type="number").text = character.currentCarriedWeight
	ET.SubElement(encumberanceWrite, "normalload", type="number").text = str(int(character.strength)*10)

	#Experience
	experienceWrite = ET.SubElement(characterWrite, "exp", type="number").text = character.experience if character.experience != "" else "0" 
	experienceNeededWrite = ET.SubElement(characterWrite, "expneeded", type="number").text = character.experienceNeeded

	#Feats
	featsWrite = ET.SubElement(characterWrite, "featlist")
	featsID = 0
	for characterFeat in character.featList:
		featsID += 1
		featsIDText = "id-0000" + str(featsID)
		featIDWrite = ET.SubElement(featsWrite, featsIDText)
		featName = characterFeat.featName
		if outputType == "dataOnlyOption":
			featDescription = characterFeat.fullDescription
			ET.SubElement(featIDWrite, "description", type="string").text = featDescription
			featShortcutWrite = ET.SubElement(featIDWrite, "shortcut", type="windowreference")
			ET.SubElement(featShortcutWrite, "class").text = ""
			ET.SubElement(featShortcutWrite, "recordname").text = ""
		if outputType == "linkedDataOption":
			featShortcutWrite = ET.SubElement(featIDWrite, "shortcut", type="windowreference")
			ET.SubElement(featShortcutWrite, "class").text = "powerdesc"
			ET.SubElement(featShortcutWrite, "recordname").text = "reference.feats." + featName.replace(" ","").lower() + "@4E PC Options"
		ET.SubElement(featIDWrite, "value", type="string").text = featName

	#Gender
	ET.SubElement(characterWrite, "gender", type="string").text = character.gender

	#Height
	ET.SubElement(characterWrite, "height", type="string").text = character.height

	#HP
	hitpointsWrite = ET.SubElement(characterWrite, "hp")
	ET.SubElement(hitpointsWrite, "bloodied", type="number").text = str(int(character.maxHp)//2)
	ET.SubElement(hitpointsWrite, "faileddeathsaves", type="number").text = "0"
	ET.SubElement(hitpointsWrite, "maxdeathsaves", type="number").text = "3"
	ET.SubElement(hitpointsWrite, "surge", type="number").text = str(int(character.maxHp)//4)
	ET.SubElement(hitpointsWrite, "surgemodifier", type="number").text = "0"
	ET.SubElement(hitpointsWrite, "surgesmax", type="number").text = character.maxSurges
	ET.SubElement(hitpointsWrite, "surgesused", type="number").text = "0"
	ET.SubElement(hitpointsWrite, "temporary", type="number").text = "0"
	ET.SubElement(hitpointsWrite, "total", type="number").text = character.maxHp
	ET.SubElement(hitpointsWrite, "wounds", type="number").text = "0"

	#Initiative
	initiativeWrite = ET.SubElement(characterWrite, "initiative")
	ET.SubElement(initiativeWrite, "misc", type="number").text = character.initiativeMiscBonus
	ET.SubElement(initiativeWrite, "temporary", type="number").text = "0"
	ET.SubElement(initiativeWrite, "total", type="number").text = character.initiative

	#Intelligence Check Modifier
	intelligencecheckmodifierWrite = ET.SubElement(characterWrite, "intelligencecheckmodifier", type="number").text = "0"

	#Inventory List
	inventoryListWrite = ET.SubElement(characterWrite, "inventorylist")
	inventoryID = 0
	for inventoryItem in character.inventoryList:
		inventoryID += 1
		inventoryIDText = "id-0000" + str(inventoryID)
		inventoryIDWrite = ET.SubElement(inventoryListWrite, inventoryIDText)
		ET.SubElement(inventoryIDWrite, "carried", type="number").text = inventoryItem.carried
		if inventoryItem.itemClass == "Magic Item" and (inventoryItem.magicItemType == "Consumable" or inventoryItem.magicItemType == "Alchemical Item"):
			ET.SubElement(inventoryIDWrite, "class", type="string").text = inventoryItem.magicItemType
		else:
			ET.SubElement(inventoryIDWrite, "class", type="string").text = inventoryItem.itemClass
		ET.SubElement(inventoryIDWrite, "count", type="number").text = inventoryItem.count
		ET.SubElement(inventoryIDWrite, "cost", type="string").text = inventoryItem.cost
		ET.SubElement(inventoryIDWrite, "flavor", type="string").text = inventoryItem.flavor
		ET.SubElement(inventoryIDWrite, "level", type="number").text = str(inventoryItem.level)
		ET.SubElement(inventoryIDWrite, "mitype", type="string").text = inventoryItem.fgmitype
		ET.SubElement(inventoryIDWrite, "name", type="string").text = inventoryItem.itemName
		ET.SubElement(inventoryIDWrite, "showonminisheet", type="number").text = str(inventoryItem.showonminisheet)
		ET.SubElement(inventoryIDWrite, "weight", type="number").text = str(inventoryItem.weight)
		ET.SubElement(inventoryIDWrite, "subclass", type="string").text = inventoryItem.subclass

	#Language List
	languageListWrite = ET.SubElement(characterWrite, "languagelist")
	langaugeID = 0
	for languageElement in character.languageRulesElements:
		langaugeID += 1
		langaugeIDText = "id-0000" + str(langaugeID)
		languageIDWrite = ET.SubElement(languageListWrite, langaugeIDText)
		languageName = languageElement.get("name")
		ET.SubElement(languageIDWrite, "name", type="string").text = languageName

	#Level and Level Bonus (1/2 level)
	ET.SubElement(characterWrite, "level", type="number").text = character.level
	ET.SubElement(characterWrite, "levelbonus", type="number").text = str(character.levelBonus)

	#Name
	nameWrite = ET.SubElement(characterWrite, "name", type="string").text = character.characterName

	#Notes
	notesWrite = ET.SubElement(characterWrite, "notes", type="string").text = character.notes

	#Power Focus
	powerFocusWrite = ET.SubElement(characterWrite, "powerfocus")
	implementPowerFocusWrite = ET.SubElement(powerFocusWrite, "implement")
	ET.SubElement(implementPowerFocusWrite, "order", type="number")
	weaponPowerFocusWrite = ET.SubElement(powerFocusWrite, "weapon")
	ET.SubElement(weaponPowerFocusWrite, "order", type="number")

	#Power Limit
	powerLimitWrite = ET.SubElement(characterWrite, "powerlimit")
	ET.SubElement(powerLimitWrite, "channeldivinity", type="number").text = "1"
	ET.SubElement(powerLimitWrite, "healinginfusion", type="number").text = "2"
	ET.SubElement(powerLimitWrite, "itemdaily", type="number").text = "1"

	#Power Mode
	ET.SubElement(characterWrite, "powermode", type="string").text = "standard"

	#Powers
	#Note: Cannot add automation as that's vary Fantasy Grounds specific
	powersWrite = ET.SubElement(characterWrite, "powers")
	powersID = 0
	for power in character.powerList:
		powerName = power.powerName
		if powerName == "Bull Rush Attack" or powerName == "Grab Attack":
			powerName = powerName.replace("Attack","")
		powersID += 1
		powerIDText = "id-0000" + str(powersID)
		powersIDWrite = ET.SubElement(powersWrite, powerIDText)
		ET.SubElement(powersIDWrite, "action", type="string").text = power.action
		ET.SubElement(powersIDWrite, "keywords", type="string").text = power.keywords
		ET.SubElement(powersIDWrite, "name", type="string").text = power.powerName
		ET.SubElement(powersIDWrite, "prepared", type="number").text = power.prepared
		ET.SubElement(powersIDWrite, "range", type="string").text = power.powerRange
		if outputType == "linkedDataOption" and (powerName != "Opportunity Attack" and powerName != "Second Wind"):
			powerShortcutWrite = ET.SubElement(powersIDWrite, "shortcut", type="windowreference")
			ET.SubElement(powerShortcutWrite, "class").text = "powerdesc"
			ET.SubElement(powerShortcutWrite, "recordname").text = "reference.powers." + power.powerName.replace(" ","").lower() + "@4E PC Options"		
		ET.SubElement(powersIDWrite, "recharge", type="string").text = power.recharge
		ET.SubElement(powersIDWrite, "shortdescription", type="string").text = power.shortdescription
		ET.SubElement(powersIDWrite, "source", type="string").text = power.source

	#Armor Proficiencies
	proficiencyarmorWrite = ET.SubElement(characterWrite, "proficiencyarmor")
	armorProficiencyID = 0
	for armorProficiencyElement in character.armorProficiencyElements:
		armorProficiencyID += 1
		armorProfIDText = "id-0000" + str(armorProficiencyID)
		armorProfIDWrite = ET.SubElement(proficiencyarmorWrite, armorProfIDText)
		armorProficiencyName = armorProficiencyElement.get("name")
		armorProficiencyREMatch = regularExpression.search(r'\((.*?)\)', armorProficiencyName)
		if armorProficiencyREMatch:
			armorProficiencyName = armorProficiencyREMatch.group(1)
		armorProfShortcutWrite = ET.SubElement(armorProfIDWrite, "shortcut", type="windowreference")
		ET.SubElement(armorProfShortcutWrite, "class")
		ET.SubElement(armorProfShortcutWrite, "recordname")
		ET.SubElement(armorProfIDWrite, "value", type="string").text = armorProficiencyName

	#Weapon Proficiencies
	proficiencyweaponWrite = ET.SubElement(characterWrite, "proficiencyweapon")
	weaponProficiencyID = 0
	for weaponProficiencyElement in character.weaponProficiencyElements:
		weaponProficiencyID += 1
		weaponProfIDText = "id-0000" + str(weaponProficiencyID)
		weaponProfIDWrite = ET.SubElement(proficiencyweaponWrite, weaponProfIDText)
		weaponProficiencyName = weaponProficiencyElement.get("name")
		weaponProficiencyName = weaponProficiencyName[weaponProficiencyName.find("(")+1:weaponProficiencyName.rfind(")")]		
		weaponProfShortcutWrite = ET.SubElement(weaponProfIDWrite, "shortcut", type="windowreference")
		ET.SubElement(weaponProfShortcutWrite, "class")
		ET.SubElement(weaponProfShortcutWrite, "recordname")
		ET.SubElement(weaponProfIDWrite, "value", type="string").text = weaponProficiencyName

	#Race and Size
	ET.SubElement(characterWrite, "race", type="string").text = character.race
	if outputType == "linkedDataOption":
		raceShortcutWrite = ET.SubElement(characterWrite, "racelink", type="windowreference")
		ET.SubElement(raceShortcutWrite, "class").text = "powerdesc"
		ET.SubElement(raceShortcutWrite, "recordname").text = "reference.races." + character.race.replace(" ","").lower() + "@4E PC Options"
	ET.SubElement(characterWrite, "size", type="string").text = character.size

	#Skills
	#Note: Class Skill defaults to 0 right now until I figure out how to do it 
	#Note: And skills don't link to a window yet. Would probably require an extension that adds a skill record category.
	skillListWrite = ET.SubElement(characterWrite, "skilllist")
	skillID = 0
	for characterSkill in character.skillList:
		skillID += 1
		skillIDText = "id-0000" + str(skillID)
		skillIDWrite = ET.SubElement(skillListWrite, skillIDText)
		ET.SubElement(skillIDWrite, "classskill", type="number").text = "0"
		ET.SubElement(skillIDWrite, "label", type="string").text = characterSkill.skillName
		ET.SubElement(skillIDWrite, "misc", type="number").text = str(characterSkill.skillMiscBonus)
		skillShortcutWrite = ET.SubElement(skillIDWrite, "shortcut", type="windowreference")
		ET.SubElement(skillShortcutWrite, "class")
		ET.SubElement(skillShortcutWrite, "recordname")
		ET.SubElement(skillIDWrite, "showonminisheet", type="number").text = "0"
		ET.SubElement(skillIDWrite, "stat", type="number").text = str(characterSkill.abilityBonus)
		ET.SubElement(skillIDWrite, "statname", type="string").text = characterSkill.skillAbility.lower()
		ET.SubElement(skillIDWrite, "total", type="number").text = str(characterSkill.totalBonus)
		ET.SubElement(skillIDWrite, "trained", type="number").text = str(characterSkill.trained)
		if characterSkill.hasArmorPenalty == "1":
			ET.SubElement(skillIDWrite, "armorPenalty", type="number").text = str(characterSkill.armorPenalty)

	#Special Abilities
	#So far concentrating on features gained at level 1, but later in other class features for essential classes or paragon paths
	specialAbilityListWrite = ET.SubElement(characterWrite, "specialabilitylist")
	specialAbilityID = 1
	##Racial Traits
	for specialAbility in character.racialTraitList:
		specialAbilityID += 1
		specialAbilityIDText = "id-0000" + str(specialAbilityID)
		specialAbilityIDWrite = ET.SubElement(specialAbilityListWrite, specialAbilityIDText)
		ET.SubElement(specialAbilityIDWrite, "description", type="string").text = specialAbility.fullDescription
		specialAbilityShortcutWrite = ET.SubElement(specialAbilityIDWrite, "shortcut", type="windowreference")
		ET.SubElement(specialAbilityShortcutWrite, "class")
		ET.SubElement(specialAbilityShortcutWrite, "recordname")
		ET.SubElement(specialAbilityIDWrite, "value", type="string").text = specialAbility.traitName
	##Class Features
	for specialAbility in character.classFeatureList:
		specialAbilityID += 1
		specialAbilityIDText = "id-0000" + str(specialAbilityID)
		specialAbilityIDWrite = ET.SubElement(specialAbilityListWrite, specialAbilityIDText)
		ET.SubElement(specialAbilityIDWrite, "description", type="string").text = specialAbility.fullDescription
		specialAbilityShortcutWrite = ET.SubElement(specialAbilityIDWrite, "shortcut", type="windowreference")
		ET.SubElement(specialAbilityShortcutWrite, "class")
		ET.SubElement(specialAbilityShortcutWrite, "recordname")
		ET.SubElement(specialAbilityIDWrite, "value", type="string").text = specialAbility.featureName


	#Speed
	speedWrite = ET.SubElement(characterWrite, "speed")
	ET.SubElement(speedWrite, "armor", type="number").text = character.armorSpeedPenalty
	ET.SubElement(speedWrite, "base", type="number").text = character.baseSpeed
	ET.SubElement(speedWrite, "final", type="number").text = character.totalSpeed
	ET.SubElement(speedWrite, "misc", type="number").text = str(int(character.totalSpeed) - (int(character.baseSpeed) + int(character.armorSpeedPenalty)))
	ET.SubElement(speedWrite, "temporary", type="number").text = "0"

	#Strength Check Modifier
	strengthcheckmodifierWrite = ET.SubElement(characterWrite, "strengthcheckmodifier", type="number").text = "0"

	#Temporary HP
	ET.SubElement(characterWrite, "temp")

	#Weapon List
	weaponListWrite = ET.SubElement(characterWrite, "weaponlist")
	
	#Weight
	ET.SubElement(characterWrite, "weight", type="string").text = character.weight

	#Wisdom Check Modifier
	wisdomcheckmodifierWrite = ET.SubElement(characterWrite, "wisdomcheckmodifier", type="number").text = "0"

	#Write Tree
	tree = ET.ElementTree(rootWrite)
	ET.indent(tree, space="\t", level=0)
	tree.write(outputFilename)

# def main() -> int:
# 	character = readCBLoaderCharacterFile("static/uploads/Ven_Tanymere.dnd4e")
# 	readCBLoaderMainFile(character)
# 	writeFantasyGroundsFile(character, None, "linkedDataOption")
# 	return 0


# if __name__ == '__main__':
# 	sys.exit(main())  # next section explains the use of sys.exit