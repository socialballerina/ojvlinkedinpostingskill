# Image library

The image files themselves are deliberately **not** committed. This repo is public, and the
library contains photographs of the four partners and, in at least one case, of event attendees
whose consent has not been recorded. `assets/images/manifest.csv` flags those as
`consent-needed`.

So the manifest is version controlled and the photographs are not.

To rebuild the library on a new machine:

1. Set `Raw image folder` in `SKILL.md` to wherever the partners drop photos.
2. Run the intake workflow: say "intake images". Each file is described, tagged and appended to
   `manifest.csv`, and copied into this directory.

The manifest already carries six rows from an earlier intake run. Those rows are accurate; the
files they name have to be restored from the original folder before they can be used.
