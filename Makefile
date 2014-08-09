# compiles coffeescript and less

MAKEFLAGS += --warn-undefined-variables

_SOURCE_DIR=client/manage_worksheets
_TARGET_DIR=manage_worksheets/static/manage_worksheets
COFFEE_FILES=$(wildcard $(_SOURCE_DIR)/*.coffee)
JS_TARGETS= $(COFFEE_FILES:$(_SOURCE_DIR)/%.coffee=$(_TARGET_DIR)/js/%.js)
LESS_FILES=$(wildcard $(_SOURCE_DIR)/*.styl)
CSS_TARGETS=$(LESS_FILES:$(_SOURCE_DIR)/%.styl=$(_TARGET_DIR)/css/%.css)

all: js css

js: $(JS_TARGETS)

css: $(CSS_TARGETS)

# make those js files
$(_TARGET_DIR)/js/%.js: $(_SOURCE_DIR)/%.coffee
	coffee -o $(_TARGET_DIR)/js/ -c $<

$(_TARGET_DIR)/css/%.css: $(_SOURCE_DIR)/%.styl
	stylus -o $(_TARGET_DIR)/css/ $<

test:
	echo $(COFFEE_FILES)
	echo $(JS_TARGETS)
