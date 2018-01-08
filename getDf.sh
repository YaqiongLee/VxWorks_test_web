cd /folk/yli14/test
./d.sh all
cat dfHead.html > df.html
sed '1,16d' defect.html >> df.html
expect dfCp.exp
