# Copyright (c) 2011, Stefano Palazzo <stefano.palazzo@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import hmac
import struct

def pbkdf2(digestmod, password, salt, count, dk_length):

    def pbkdf2_function(pw, salt, count, i):
        r = u = hmac.new(pw, salt + struct.pack(">i", i), digestmod).digest()
        for i in range(2, count + 1):
            u = hmac.new(pw, u, digestmod).digest()
            r = bytes(i ^ j for i, j in zip(r, u))
        return r
    dk, h_length = b'', digestmod().digest_size
    blocks = (dk_length // h_length) + (1 if dk_length % h_length else 0)
    for i in range(1, blocks + 1):
        dk += pbkdf2_function(password, salt, count, i)
        
    return dk[:dk_length]
