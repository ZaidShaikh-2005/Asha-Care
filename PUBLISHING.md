# Publish the ASHA Care README

## 1. Update the repository

Copy `README.md` and the complete `docs/` folder into the root of
`ZaidShaikh-2005/community-help`, then commit them.
Keep the paths exactly as supplied so the download button, GIF, and screenshot render.

## 2. Publish the installer

1. Open the repository on GitHub and go to **Releases → Create a new release**.
2. Create the tag **v1.1.1** and use **ASHA Care v1.1.1** as the release title.
3. Attach `release-assets/AshaNurseApp_Setup_v1.1.1.exe` as a release asset.
4. Publish the release.

The README button links directly to:

https://github.com/ZaidShaikh-2005/community-help/releases/download/v1.1.1/AshaNurseApp_Setup_v1.1.1.exe

Upload the installer through Releases; `release-assets/` does not need to be committed
with the source code. The download button becomes active once the release asset exists.
If the repository is private, the viewer needs access to download the installer.

## Included visuals

- `docs/media/download-windows.svg`: Download button, version 1.1.1.
- `docs/media/asha-care-preview.gif`: A 12-second looping dashboard highlight preview.
- `docs/media/dashboard.png`: Static dashboard preview.

The GIF uses the supplied application screenshot with animated highlights. It is a
visual preview, rather than a recording of clicks or navigation. The screenshot crop
ends before the table containing individual member details.
