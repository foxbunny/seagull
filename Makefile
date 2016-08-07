SKIN := seagull

# Base paths
SKIN_DIR = seagull/skins/$(SKIN)
SRC_DIR = $(SKIN_DIR)/src
OUTPUT_DIR = $(SKIN_DIR)/assets

# Assets config
BASE_URL = /static/
SCSS_DIR = $(SRC_DIR)/scss
COFFEE_DIR = $(SRC_DIR)/coffee
CSS_DIR = $(OUTPUT_DIR)/css
JS_DIR = $(OUTPUT_DIR)/js
JS_KEEP = $(JS_DIR)/vendor
IMG_DIR = $(OUTPUT_DIR)/img
FONT_DIR = $(OUTPUT_DIR)/font

# Compass configuration
COMPASS_STYLE = expanded
COMPASS_EXTRA_ARGS = --relative-assets
COMPASS_ARGS = --http-path "$(BASE_URL)"
COMPASS_ARGS += --app-dir "$(SKIN_DIR)"
COMPASS_ARGS += --sass-dir "$(SCSS_DIR)"
COMPASS_ARGS += --css-dir "$(CSS_DIR)"
COMPASS_ARGS += --images-dir "$(IMG_DIR)"
COMPASS_ARGS += --javascripts-dir "$(JS_DIR)"
COMPASS_ARGS += --fonts-dir "$(FONT_DIR)"
COMPASS_ARGS += --output-style "$(COMPASS_STYLE)"
COMPASS_ARGS += $(COMPASS_EXTRA_ARGS)
COMPASS_COMPILE = compass compile --force
COMPASS_WATCH = compass watch

# CoffeeScript configuration
COFFEE_ARGS = --bare
COFFEE_ARGS += --output $(JS_DIR)
COFFEE_ARGS += $(COFFEE_DIR)
COFFEE_COMPILE = coffee --compile
COFFEE_WATCH = coffee --watch

# PID files
TMPDIR = /tmp
COMPASS_PID = $(TMPDIR)/.compass_pid
COFFEE_PID = $(TMPDIR)/.coffee_pid
FSAL_PID = $(TMPDIR)/.fsal_pid

.PHONY: \
	start \
	stop \
	restart \
	recompile \
	stop-compass \
	stop-coffee

start: $(COMPASS_PID) $(COFFEE_PID)

stop: stop-compass stop-coffee

restart: stop-assets watch-assets

recompile:
	@$(COMPASS_COMPILE) $(COMPASS_ARGS)
	@find $(JS_DIR) -path $(JS_KEEP) -prune -o -name "*.js" -exec rm {} +
	@$(COFFEE_COMPILE) $(COFFEE_ARGS)

stop-compass:
	@-kill -s TERM $$(cat $(COMPASS_PID))
	@-rm $(COMPASS_PID)

stop-coffee:
	@-kill -s INT $$(cat $(COFFEE_PID))
	@-rm $(COFFEE_PID)

$(COMPASS_PID): $(TMPDIR)
	@$(COMPASS_WATCH) $(COMPASS_ARGS) & echo $$! > $@

$(COFFEE_PID): $(TMPDIR)
	@$(COFFEE_WATCH) $(COFFEE_ARGS) & echo $$! > $@
