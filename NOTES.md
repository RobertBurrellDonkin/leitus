In Flight

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

TODO:
 * Improve error handling from cryptsetup by checking for 255 status (wrong password, looks like) 
 * Replace logged description of disc with message loaded from json
 * Bash completion
 * Add --list-drives (which lists drives)
 * Validate configurations
 * Add luks drive creation
 * Add option to zero new drives in addition to default use of dev random
 * Improve error reporting when disc image already in use
 * Improve error handling from cryptsetup by checking for 240 (device is busy) 
 * Check drives before mounting