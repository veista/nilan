# Marketing name aliases (CTS602 HMI)

Maps [nilan.no](https://www.nilan.no/produkter) marketing names to HMI type names / ids already known in code. Aliases do not add new Modbus maps. Unknown type ids stay `needs_dump`.

| Marketing / plate text | Prefer HMI name | Type id | Guide |
|---|---|---|---|
| Comfort CT200, Comfort light | Comfort light | 2 | [comfort-light](../cts602/comfort-light.md) |
| Comfort Polar, Combi Polar (legacy naming) | Comfort Polar | 3 | [comfort-polar](../cts602/comfort-polar.md) |
| Comfort 200/250/350 Top, 300LR, 250L/R, 350L/R, 450, CT500 | COMFORT / COMFORTn | 13 / 31 | [comfort](../cts602/comfort.md) · [comfortn](../cts602/comfortn.md) |
| VPL 15, VPL 15 Top M2 | VPL 15c | 4 | [vpl-15c](../cts602/vpl-15c.md) |
| VPL 25 | VPL 25c | 25 | [vpl-25c](../cts602/vpl-25c.md) |
| VPL 28 (bolig-sized) | VPM/28EC | 26 | [vpm-28ec](../cts602/vpm-28ec.md) |
| Compact S | CompactS | 10 | [compacts](../cts602/compacts.md) |
| Compact P (CTS602), Compact P AIR/GEO/EK/Nordic/XL, Compact P2* | CompactP | 44 | [compactp](../cts602/compactp.md) · [compact-p2](../cts602/compact-p2.md) · [compact-p-xl-nordic](compact-p-xl-nordic.md) |
| Compact P XL Nordic (CTS602 RS485 plate only) | CompactP | 44 | [compactp](../cts602/compactp.md) · [compact-p-xl-nordic](compact-p-xl-nordic.md) |
| Compact P Køl Polar/Nordic/Arctic (XL), Nordic XL RF, NCS-700 LC (4747=101–104) | CTS700_NORDIC | n/a | [cts700/compact-p-nordic-xl](../cts700/compact-p-nordic-xl.md) · [hardware](../cts700/hardware/) |
| Compact P (CTS700 Ethernet 2018+) | CTS700 Compact P | n/a | [cts700/compact-p](../cts700/compact-p.md) |
| VP 18 M2 | VP18 M2 | 32 | [vp18-m2](../cts602/vp18-m2.md) |
| VP 18 M2 EK, VP 18 EK | VP 18ek / VP 18cek | 20 / 21 | [vp-18ek](../cts602/vp-18ek.md) |
| Combi 302 Polar | COMBI 302 | 35 | [combi-302](../cts602/combi-302.md) |
| Combi 302 Polar Top | COMBI 302 T | 36 | [combi-302-t](../cts602/combi-302-t.md) |
| Combi S 302 Polar Top | COMBI 300 N | 33 | [combi-300-n](../cts602/combi-300-n.md) |
| Combi 400 Polar Top | unknown | | Dump required |
| VGU 180 EK | VGU180 ek | 38 | [vgu180-ek](../cts602/vgu180-ek.md) |
| VGU 250 M2 Nordic | unknown | | Dump required |
| Comfort 600 / 1200 / 5000 (næring) | CTS602 commercial | unknown | [naering](../naering/README.md) |
| VR / VPR / VPM commercial | CTS602 commercial | unknown | [naering](../naering/README.md) |

Python mirror: `custom_components/nilan/capabilities.py` (`MARKETING_ALIASES`).
