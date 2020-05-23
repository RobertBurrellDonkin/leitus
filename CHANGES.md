Changes
=======

Leitus 2.0
 * Change default configuration director to `/etc/leitus.d`
 
Letius 1.1
 * https://github.com/RobertBurrellDonkin/leitus/issues/13 Check drive before mounting Issue 

Leitus 1.0
 * Port to Python 3

Leitus 0.6
 * Adopt simpler and more pythonic package name
 * Adopt more conventional directory structure: move script into bin
  
Leitus 0.5
 * Add "leitus <name> --info" which lists configuration information on <name>
 * Improved error reporting when losetup command isn't available
 * Generate anonymous drive in /tmp (not current directory)
 * Improved error reporting when passphrase is mistyped
 * Upgraded to Python 3
 * Improved error reporting when user hasn't permission to read the
   configuration
 * Improved error reporting when drive is already in use

Leitus 0.4
 * Improved --help
  * Include version number in --help
  * Print configuration properties in --help
 * Replace script default action (create new image) with version number and wacky comment
 * Clean out aboriginal sources
 * Improve error reporting when disc image not found
 * Support absolute paths for disc images, not just those in drives.d
 * Add support for loopback image drive configurations
 
Leitus 0.3
 * Improved error reporting:
   * When configuration file not found
   * When script cancelled from keyboard

