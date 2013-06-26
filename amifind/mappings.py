"""
dicts that maps EC2 API filter values to more concise names (e.g., x86_64 -> 64)
"""

operating_systems = {
    'Windows': 'windows',
    'windows': 'windows',
    'linux': 'linux'
}
""" Supported values for os filter """

architectures = {
    '32': 'i386',
    'i386': 'i386',
    '64': 'x86_64',
    'x86_64': 'x86_64'
}
""" Supported values for arch filter"""

virtualization_types = {
    'hvm': 'hvm',
    'pv': 'paravirtual',
    'paravirtual': 'paravirtual'
}
""" Supported values for virt_type filter """

root_device_types = {
    'ebs': 'ebs',
    's3': 'instance-store',
    'instance-store': 'instance-store'
}
""" Supported values for root_dev_type """

just_one = {
    'first' : 0,
    'last' : -1
}
""" Indexes for first and last items """