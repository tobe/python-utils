#!/usr/bin/env python

from Tkinter import Tk
from tkFileDialog import askopenfilename
import tkMessageBox
import os.path
import ConfigParser
import shutil

def main():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(initialdir='D:/install/LoL/League of Legends', title='lolfpsfix', defaultextension='.exe', filetypes=[('lol.launcher.exe', 'lol.launcher.exe')]) # Look for lol.launcher.exe

    if not filename: exit('Nothing chosen!')

    # Get the directory from the file.
    directory = filename[:-16] # Remove lol.launcher.exe.
    cfg       = directory + 'Config/game.cfg'

    # Check if the game.cfg is present.
    if not os.path.isfile(cfg):
        tkMessageBox.showerror('Open file', 'Cannot find game.cfg!')
        return

    # Try to parse game.cfg
    config             = ConfigParser.RawConfigParser()
    config.optionxform = str

    try:
        config.read(cfg)
    except ConfigParser.ParsingError, e:
        tkMessageBox.showerror('ConfigParser', 'Cannot parse game.cfg: ' + e)
        return

    # Now make a backup.
    try:
        shutil.copyfile(cfg, directory + 'Config/game.cfg.bak')
    except IOError, e:
        tkMessageBox.showerror('shutil', 'Could not make a backup of the original file: ' + e)
        return

    # Append the "safe settings" first.
    if not config.has_section('UnitRenderStyle'):
        config.add_section('UnitRenderStyle')

    config.set('UnitRenderStyle', 'Inking', '0')
    config.set('UnitRenderStyle', 'AdvancedReflection', '0')
    config.set('UnitRenderStyle', 'PerPixelPointLightning', '0')

    # Write.
    try:
        with open(cfg, 'wb') as cfg_file:
            config.write(cfg_file)
    except:
        tkMessageBox.showerror('ConfigParser', 'An error occured. Could not write to game.cfg.')
        return

    # Inform the user that all is well and ask about further optimizations.
    if not tkMessageBox.askyesno('lolfpsfix', 'Patched successfully! Would you like to proceed with further optimizations?\nThese will make your game look very ugly, however you should gain more FPS.'):
        return # Bye, bye.

    # Futher optimizations are below.
    config.set('General', 'EnableLightFX', '0') # Disable LightFX (?)
    config.set('General', 'Colors', '16') # Change colors from 32bit to 16bit
    config.set('General', 'WaitForVerticalSync', '0') # Do NOT wait for VSync, instead we'll cap the FPS to 100.
    config.set('Performance', 'ShadowsEnabled', '0') # Disable shadows.
    config.set('Performance', 'EnableHUDAnimations', '0') # Disable HUD animations.
    config.set('Performance', 'EnableParticleOptimizations', '0') # This apparently increases FPS.
    config.set('Performance', 'EnableGrassSwaying', '0') # Disable grass movement.
    config.set('Performance', 'EnableFXAA', '0') # Disable Fast Approximate Anti-Aliasing.
    config.set('Performance', 'AdvancedShader', '0') # Disable Advanced shaders.
    config.set('Performance', 'FrameCapType', '6') # 100fps lock. Saves GPU from suffering.
    config.set('Performance', 'EffectsQuality', '0') # Lowest effects quality.
    config.set('Performance', 'EnvironmentQuality', '0') # Lowest environment quality.
    config.set('Performance', 'CharacterQuality', '0') # Lowest character quality.
    config.set('Performance', 'AutoPerformanceSettings', '0') # Disable Auto optimizations.
    config.set('Performance', 'ShadowsQuality', '0') # Worst shadows ever.
    config.set('Performance', 'GraphicsSlider', '0') # ???
    config.set('Performance', 'Inking', '0') # Take off the "new" graphics.
    config.set('Performance', 'PerPixelPointLightning', '0') # Disable lightning per pixel.
    config.set('Performance', 'AdvancedReflection', '0') # Remove the advanced reflection.

    # Write again...
    try:
        with open(cfg, 'wb') as cfg_file:
            config.write(cfg_file)
    except:
        tkMessageBox.showerror('ConfigParser', 'An error occured. Could not write to game.cfg.')
        return

    # Wohoo.
    tkMessageBox.showinfo('lolfpsfix', 'Patched successfully! (x2)')

if __name__ == '__main__':
    main()