from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class StaticStorage(ManifestStaticFilesStorage):
    patterns = (
        # taken from Django sources:
        ("*.css", (
            r"""(url\(['"]{0,1}\s*(.*?)["']{0,1}\))""",
            (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
        )),

        # added by me:
        ("*.js", (
            (
                r"""(//#\s*sourceMappingURL=(.*)$)""",
                """//# sourceMappingURL=%s"""
            ),
        )),
    )
