HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_versioning',
        'djangocms_formbuilder',
    ],
}


def run():
    from app_helper import runner

    runner.cms('djangocms_formbuilder')


if __name__ == "__main__":
    run()
