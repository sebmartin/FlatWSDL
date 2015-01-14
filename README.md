A small python script that will fetch a WSDL from a URL and flatten it by importing all referenced parts (external files) into a single WSDL file. This is especially useful for working with WCF based services which are notorious for splitting a WSDL definition into several nested files. This script will allow your WSDL to be used with proxy generators that cannot resolve or can't access the URLs that are in your original WSDL file.

#License
This code is public domain.  Use the script (and generated artifacts) as you see fit as long as it's for good and not evil.
