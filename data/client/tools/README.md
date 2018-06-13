AUVSI SUAS: Interoperability Client Tools
=========================================

interop_cli.py
--------------

<<<<<<< HEAD
This command line tool can be used to get mission details, upload odlcs,
=======
This command line tool can be used to get mission details, upload targets,
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
probe the server with dummy data, and forward MAVLink packets to interop.

```
URL=http://10.10.130.2:8000
USER=testuser
./interop_cli.py --url $URL --username $USER missions
<<<<<<< HEAD
./interop_cli.py --url $URL --username $USER odlcs \
    --odlc_filepath tools/testdata/odlcs.txt \
=======
./interop_cli.py --url $URL --username $USER targets \
    --target_filepath tools/testdata/targets.txt \
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
    --imagery_dir tools/testdata/
./interop_cli.py --url $URL --username $USER probe
./interop_cli.py --url $URL --username $USER mavlink --device 127.0.0.1:14550
```

Target Uploads
--------------

Uploader Limitations:
<<<<<<< HEAD
* Only non-ADLC odlcs.
=======
* Only non-ADLC targets.
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
* Only upload (POST), no retrieval (GET) or removal (DELETE).
* Only performs format conversion, not client-side data validation. Invalid
  data (e.g. invalid shape) will attempt to be uploaded, and the server will
  reject it.
* Does not detect duplicates- executing the script twice will upload two sets
<<<<<<< HEAD
  of odlcs.
=======
  of targets.
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

MAVLink Forward
---------------

The MAVLink forwarding will quit on an error. To automatically retry, wrap the
command in a while loop.

```
while true; do [command]; done
```
