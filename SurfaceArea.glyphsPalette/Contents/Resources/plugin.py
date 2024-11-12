# encoding: utf-8

###########################################################################################################
#
#
# Palette Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import * #Glyphs, GSEditViewController, UPDATEINTERFACE
from GlyphsApp.plugins import PalettePlugin


class SurafceArea (PalettePlugin):

	dialog = objc.IBOutlet()
	textField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Surface area',
			'de': 'Oberflächeninhalt',
			'fr': 'Surface',
		})
		self.error = Glyphs.localize({
			'en': 'An error occured',
			'de': 'Es gab einen Fehler',
			'fr': 'Une erreur s’est produite',
		})
		self.errorTips = Glyphs.localize({
			'en': 'Calculation stopped',
			'de': 'Berechnung unterbrochen',
			'fr': 'Calcul interrompu',
		})
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)

	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)

	@objc.python_method
	def update(self, sender):

		text = [""]
		# Extract font from sender
		currentTab = sender.object()
		# We’re in the Edit View
		if isinstance(currentTab, GSEditViewController):
			# Check whether glyph is being edited
			layer = currentTab.activeLayer()
			if layer is not None:
				if layer.shapes is not None:
					area = 0
					shp = []
					try:
						for shape in layer.shapes:
							shp.append(shape)
					except: 
						 Message(self.errorTips, title='Info', OKButton="OK")
					if (shp != []):
						try:
							shpArea = removeOverlap(shp)
							for shp in shpArea:
								area += shp.area()
								text[0] = (self.name + ': %s' % (int(area)))
						except:
							text[0] = (self.error + ': %s' % (self.errorTips))
					
		# We’re in the Font view
		else:
			try:
				text.append('Selected glyphs: %s' % len(currentTab.selectedLayers))
			except:
				pass

		# Send text to dialog to display
		self.textField.setStringValue_('\n'.join(text))

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
