"""
This package provides methods to locate the current version of an Amazon
Machine Image based on some metadata about that image. An example
of a common use case would be to locate the latest AMI for the EBS-backed,
64-bit Windows Server 2008 R2 image.

This package uses boto and all of its conventions for specifying
AWS API credentials (i.e., Access Key and Secret Key).
"""
import amifilter
import search
import exceptions
import searchresult
import util