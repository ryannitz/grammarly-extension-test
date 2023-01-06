#extensions page shadow dowm selectors
menu_bars = "return document.querySelector('extensions-manager').shadowRoot.querySelector('extensions-toolbar').shadowRoot.querySelector('cr-toolbar').shadowRoot.querySelector('#menuButton')"
extension_list_container = "return document.querySelector('extensions-manager').shadowRoot.querySelector('#items-list')"

#grammarly shadow dom selectors
grammarly_card = "return document.querySelector('extensions-manager').shadowRoot.querySelector('#items-list').shadowRoot.querySelector('#kbfnbcaeplbcioakkpcpgfkobkghlhen')"
grammarly_card_check = "return document.querySelector('extensions-manager').shadowRoot.querySelector('#items-list').shadowRoot.querySelector('#kbfnbcaeplbcioakkpcpgfkobkghlhen').shadowRoot.querySelector('#card')"
grammarly_highlight = """return document.querySelector('#form > div > grammarly-extension:nth-child(2)').shadowRoot.querySelector('[data-grammarly-part="highlight"]')"""
grammarly_suggested_correction = """return document.querySelector('grammarly-mirror').shadowRoot.querySelector('[data-grammarly-part="replacement-card-item"]')"""

#wordcounter page selectors
wc_text_area = "box"
