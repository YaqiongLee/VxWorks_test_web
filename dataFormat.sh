sed 's/\(.*    \).*/\1/' /folk/yli14/nightly.ini > /folk/yli14/test/nightlyNew.ini
cd /folk/yli14/test/
oldstr="\["
newstr="\[TestCase"
cat nightlyNew.ini | sed -n "s/$oldstr/$newstr/g;p" > nightlyR.ini
rm -rf /folk/yli14/test/nightlyNew.ini
