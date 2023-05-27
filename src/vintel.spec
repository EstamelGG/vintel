# -*- mode: python -*-
import sys

app_name = 'vintel-1.2.7.5'
block_cipher = None

a = Analysis(['vintel.py'],
             #!!!should Edit Path!!!
             pathex=['C:\\Users\\HP\\PycharmProjects\\vintel\\src' if sys.platform == 'win32' else '/Users/mark/code/vintel/src'],
             binaries=None,
             datas=None,
             hookspath=[],
             hiddenimports=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

a.datas += [('vi/ui/MainWindow.ui', 'vi/ui/MainWindow.ui', 'DATA'),
            ('vi/ui/SystemChat.ui', 'vi/ui/SystemChat.ui', 'DATA'),
            ('vi/ui/ChatEntry.ui', 'vi/ui/ChatEntry.ui', 'DATA'),
            ('vi/ui/Info.ui', 'vi/ui/Info.ui', 'DATA'),
            ('vi/ui/RefreshMap.ui', 'vi/ui/RefreshMap.ui', 'DATA'),
            ('vi/ui/ChatroomsChooser.ui', 'vi/ui/ChatroomsChooser.ui', 'DATA'),
            ('vi/ui/RegionChooser.ui', 'vi/ui/RegionChooser.ui', 'DATA'),
            ('vi/ui/SoundSetup.ui', 'vi/ui/SoundSetup.ui', 'DATA'),
            ('vi/ui/JumpbridgeChooser.ui', 'vi/ui/JumpbridgeChooser.ui', 'DATA'),
            ('vi/ui/res/qmark.png', 'vi/ui/res/qmark.png', 'DATA'),
            ('vi/ui/res/logo.png', 'vi/ui/res/logo.png', 'DATA'),
            ('mapSVG/map_Aridia.svg', 'mapSVG/map_Aridia.svg', 'DATA'),
            ('mapSVG/map_Black_Rise.svg', 'mapSVG/map_Black_Rise.svg', 'DATA'),
            ('mapSVG/map_The_Bleak_Lands.svg', 'mapSVG/map_The_Bleak_Lands.svg', 'DATA'),
            ('mapSVG/map_Branch.svg', 'mapSVG/map_Branch.svg', 'DATA'),
            ('mapSVG/map_Cache.svg', 'mapSVG/map_Cache.svg', 'DATA'),
            ('mapSVG/map_Catch.svg', 'mapSVG/map_Catch.svg', 'DATA'),
            ('mapSVG/map_The_Citadel.svg', 'mapSVG/map_The_Citadel.svg', 'DATA'),
            ('mapSVG/map_Cloud_Ring.svg', 'mapSVG/map_Cloud_Ring.svg', 'DATA'),
            ('mapSVG/map_Cobalt_Edge.svg', 'mapSVG/map_Cobalt_Edge.svg', 'DATA'),
            ('mapSVG/map_Curse.svg', 'mapSVG/map_Curse.svg', 'DATA'),
            ('mapSVG/map_Deklein.svg', 'mapSVG/map_Deklein.svg', 'DATA'),
            ('mapSVG/map_Delve.svg', 'mapSVG/map_Delve.svg', 'DATA'),
            ('mapSVG/map_Derelik.svg', 'mapSVG/map_Derelik.svg', 'DATA'),
            ('mapSVG/map_Detorid.svg', 'mapSVG/map_Detorid.svg', 'DATA'),
            ('mapSVG/map_Devoid.svg', 'mapSVG/map_Devoid.svg', 'DATA'),
            ('mapSVG/map_Domain.svg', 'mapSVG/map_Domain.svg', 'DATA'),
            ('mapSVG/map_Esoteria.svg', 'mapSVG/map_Esoteria.svg', 'DATA'),
            ('mapSVG/map_Essence.svg', 'mapSVG/map_Essence.svg', 'DATA'),
            ('mapSVG/map_Etherium_Reach.svg', 'mapSVG/map_Etherium_Reach.svg', 'DATA'),
            ('mapSVG/map_Everyshore.svg', 'mapSVG/map_Everyshore.svg', 'DATA'),
            ('mapSVG/map_Fade.svg', 'mapSVG/map_Fade.svg', 'DATA'),
            ('mapSVG/map_Feythabolis.svg', 'mapSVG/map_Feythabolis.svg', 'DATA'),
            ('mapSVG/map_The_Forge.svg', 'mapSVG/map_The_Forge.svg', 'DATA'),
            ('mapSVG/map_Fountain.svg', 'mapSVG/map_Fountain.svg', 'DATA'),
            ('mapSVG/map_Geminate.svg', 'mapSVG/map_Geminate.svg', 'DATA'),
            ('mapSVG/map_Genesis.svg', 'mapSVG/map_Genesis.svg', 'DATA'),
            ('mapSVG/map_Great_Wildlands.svg', 'mapSVG/map_Great_Wildlands.svg', 'DATA'),
            ('mapSVG/map_Heimatar.svg', 'mapSVG/map_Heimatar.svg', 'DATA'),
            ('mapSVG/map_Immensea.svg', 'mapSVG/map_Immensea.svg', 'DATA'),
            ('mapSVG/map_Impass.svg', 'mapSVG/map_Impass.svg', 'DATA'),
            ('mapSVG/map_Insmother.svg', 'mapSVG/map_Insmother.svg', 'DATA'),
            ('mapSVG/map_Kador.svg', 'mapSVG/map_Kador.svg', 'DATA'),
            ('mapSVG/map_The_Kalevala_Expanse.svg', 'mapSVG/map_The_Kalevala_Expanse.svg', 'DATA'),
            ('mapSVG/map_Khanid.svg', 'mapSVG/map_Khanid.svg', 'DATA'),
            ('mapSVG/map_Kor-azor.svg', 'mapSVG/map_Kor-azor.svg', 'DATA'),
            ('mapSVG/map_Lonetrek.svg', 'mapSVG/map_Lonetrek.svg', 'DATA'),
            ('mapSVG/map_Malpais.svg', 'mapSVG/map_Malpais.svg', 'DATA'),
            ('mapSVG/map_Metropolis.svg', 'mapSVG/map_Metropolis.svg', 'DATA'),
            ('mapSVG/map_Molden_Heath.svg', 'mapSVG/map_Molden_Heath.svg', 'DATA'),
            ('mapSVG/map_Oasa.svg', 'mapSVG/map_Oasa.svg', 'DATA'),
            ('mapSVG/map_Omist.svg', 'mapSVG/map_Omist.svg', 'DATA'),
            ('mapSVG/map_Outer_Passage.svg', 'mapSVG/map_Outer_Passage.svg', 'DATA'),
            ('mapSVG/map_Outer_Ring.svg', 'mapSVG/map_Outer_Ring.svg', 'DATA'),
            ('mapSVG/map_Paragon_Soul.svg', 'mapSVG/map_Paragon_Soul.svg', 'DATA'),
            ('mapSVG/map_Period_Basis.svg', 'mapSVG/map_Period_Basis.svg', 'DATA'),
            ('mapSVG/map_Perrigen_Falls.svg', 'mapSVG/map_Perrigen_Falls.svg', 'DATA'),
            ('mapSVG/map_Placid.svg', 'mapSVG/map_Placid.svg', 'DATA'),
            ('mapSVG/map_Pochven.svg', 'mapSVG/map_Pochven.svg', 'DATA'),
            ('mapSVG/map_Providence.svg', 'mapSVG/map_Providence.svg', 'DATA'),
            ('mapSVG/map_Pure_Blind.svg', 'mapSVG/map_Pure_Blind.svg', 'DATA'),
            ('mapSVG/map_Querious.svg', 'mapSVG/map_Querious.svg', 'DATA'),
            ('mapSVG/map_Scalding_Pass.svg', 'mapSVG/map_Scalding_Pass.svg', 'DATA'),
            ('mapSVG/map_Sinq_Laison.svg', 'mapSVG/map_Sinq_Laison.svg', 'DATA'),
            ('mapSVG/map_Solitude.svg', 'mapSVG/map_Solitude.svg', 'DATA'),
            ('mapSVG/map_The_Spire.svg', 'mapSVG/map_The_Spire.svg', 'DATA'),
            ('mapSVG/map_Stain.svg', 'mapSVG/map_Stain.svg', 'DATA'),
            ('mapSVG/map_Syndicate.svg', 'mapSVG/map_Syndicate.svg', 'DATA'),
            ('mapSVG/map_Tash-murkon.svg', 'mapSVG/map_Tash-murkon.svg', 'DATA'),
            ('mapSVG/map_Tenal.svg', 'mapSVG/map_Tenal.svg', 'DATA'),
            ('mapSVG/map_Tenerifis.svg', 'mapSVG/map_Tenerifis.svg', 'DATA'),
            ('mapSVG/map_Tribute.svg', 'mapSVG/map_Tribute.svg', 'DATA'),
            ('mapSVG/map_Vale_Of_The_Silent.svg', 'mapSVG/map_Vale_Of_The_Silent.svg', 'DATA'),
            ('mapSVG/map_Venal.svg', 'mapSVG/map_Venal.svg', 'DATA'),
            ('mapSVG/map_Verge_Vendor.svg', 'mapSVG/map_Verge_Vendor.svg', 'DATA'),
            ('mapSVG/map_Wicked_Creek.svg', 'mapSVG/map_Wicked_Creek.svg', 'DATA'),
            ('vi/ui/res/logo_small.png', 'vi/ui/res/logo_small.png', 'DATA'),
            ('vi/ui/res/logo_small_green.png', 'vi/ui/res/logo_small_green.png', 'DATA'),
            ('vi/ui/res/178028__zimbot__bosun-whistle-sttos-recreated.wav', 'vi/ui/res/178028__zimbot__bosun-whistle-sttos-recreated.wav', 'DATA'),
            ('vi/ui/res/178031__zimbot__transporterstartbeep0-sttos-recreated.wav', 'vi/ui/res/178031__zimbot__transporterstartbeep0-sttos-recreated.wav', 'DATA'),
            ('vi/ui/res/178032__zimbot__redalert-klaxon-sttos-recreated.wav', 'vi/ui/res/178032__zimbot__redalert-klaxon-sttos-recreated.wav', 'DATA'),
            ('vi/ui/res/mapdata/Providencecatch.svg', 'vi/ui/res/mapdata/Providencecatch.svg', 'DATA'),
            ('docs/jumpbridgeformat.txt', 'docs/jumpbridgeformat.txt', 'DATA'),
            ]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', app_name + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          console=False,
          #debug=True,
          #console=True,
          strip=False,
          icon='icon.ico',
          upx=False,
          cipher=block_cipher)

# Build a .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name=app_name + '.app',
                icon='icon.ico')
