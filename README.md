# How to Use

```bash
    ./geoip-quantizer.py /var/log/apache2/access.log /var/log/apache2/access,log.1
```

It should produce a sorted list of country name, country code,
and count of lines (IPs) from that country.

It can also operate on streamed input:

```bash
    cat /var/log/apache2/access.log | ./geoip-quantizer.py
    ./geoip-quantizer.py -
```

where the second example using `-` will read from `stdin`.

# Caveats

This program ignores any hits from IPs that have a "None" country type.

This program does not double-count multiple visits from any IP.  It works
off of a unique set of IPs that it comes across while parsing the logs.

# License

All source code is released under the MIT License (see [LICENSE](LICENSE)).
