
Create a following function:

As an input you have several entities, so called "creatives". Each of them has
   - price
   - id of advertiser
   - country name to serve (optional)

Please implement a function auction, receiving
   - array of creatives
   - number of winners
   - country name (optional)

and returning winner creatives, obeying the following rules:


1. all winners must have unique advertiser id
2. if third argument (country) is provided, then only creatives
without country or creatives with same country can be among winners
3. function should not give preference to any of equal by price
creatives, but should return such creatives equiprobable.

Please cover your solution with tests  .

---

* Consider a case with several input creatives equal by price and
several function calls with same input, output results may be
different
