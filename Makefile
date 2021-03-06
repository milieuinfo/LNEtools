#/***************************************************************************
# LNEtools
#
# LNE-tools voor QGIS
#							 -------------------
#		begin				: 2016-01-27
#		git sha				: $Format:%H$
#		copyright			: (C) 2016 by Kay Warrie
#		email				: kaywarrie@gmail.com
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
# LOCALES = af
LOCALES =

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
#LRELEASE = lrelease
#LRELEASE = lrelease-qt4


# translation
SOURCES = \
	__init__.py LNEtools_BlootstellingZiekenhuis.py \
	LNEtools.py LNEtools_bufferELFbronnen.py LNEtools_provider.py

PLUGINNAME = Processing_Tools_voor_LNE

PY_FILES = \
	__init__.py  LNEtools_BlootstellingZiekenhuis.py \
	LNEtools.py LNEtools_bufferELFbronnen.py LNEtools_provider.py

EXTRAS = metadata.txt pics algoritmHelper

UI_FILES =

RESOURCE_FILES =

QGISDIR =.qgis2

PLUGIN_UPLOAD = $(c)/scripts/plugin_upload.py

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%_rc.py : %.qrc $(RESOURCES_SRC)
	pyrcc4 -o $*.py  $<

%.py : %.ui
	#pyuic4 -o $@ $<
	python C:\OSGeo4W64\apps\Python27\lib\site-packages\PyQt4\uic\pyuic.py -o $@ $<

%.qm : %.ts
	$(LRELEASE) $<

deploy: compile transcompile
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $HOME/$(QGISDIR)/python/plugins
	if [ -d "$(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)" ]; then rm -r $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME); fi
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	#cp -vf $(UI_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	#cp -vf $(RESOURCE_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr $(EXTRAS) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr i18n $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
dclean:
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".git" -prune -exec rm -Rf {} \;

derase:
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

zip: deploy
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/build/$(PLUGINNAME).zip $(PLUGINNAME)

package: compile
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

upload: zip
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

transup:
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@chmod +x scripts/compile-strings.sh
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	rm -f i18n/*.qm

clean:
	rm $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

