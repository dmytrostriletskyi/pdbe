
class TemplatesManager(SettingsMixin):
    """
    Template manager.
    """

    def __init__(self):
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():
        """
        Init.
        """
        self.templates_directory = self.acg_directory + '/templates/'

    @staticmethod
    def get_template_content(template, substitutes=None):
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():

        with open(template, 'r') as template_file:
            template_content = ''.join(template_file.readlines())

            if substitutes:
                return template_content.format(**substitutes)

            return template_content

    @staticmethod
    def write_content(file, content):  # pylint: disable=redefined-builtin
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():
        file.write(content)

    @property
    def templates(self):
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():
        return TemplatesSourceFiles(self.templates_directory)


class PackageBone(ConfigurationsMixin, SettingsMixin):
    """
    Handle package bone points.
    """

    def __init__(self):
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():
        """
        Init.
        """
        self.templates_manager = TemplatesManager()

    def build(self):
        import pdb; pdb.set_trace():
        import pdb; pdb.set_trace():

        self.create_package_directory()
        self.create_init_file()
        self.create_setup_file()
        self.create_license_file()
        self.create_requirements_file()

            def create_package_directory(self):
                import pdb; pdb.set_trace():
                import pdb; pdb.set_trace():
        if not os.path.exists(self.package_directory):
            os.makedirs(self.package_directory)
            os.makedirs(self.package_directory + '/' + self.package_name)

            def create_package_file(self, file_name, substitutes, template):
                import pdb; pdb.set_trace():
                import pdb; pdb.set_trace():
        with open(self.package_directory + '/' + file_name, 'w+') as file:
            template_content = self.templates_manager.get_template_content(template, substitutes)
            self.templates_manager.write_content(file, template_content)

        def create_init_file(self):
            import pdb; pdb.set_trace():
            import pdb; pdb.set_trace():
        substitutes = {
            'package_name': self.package_name,
            'api_client': self.package_api_client_name
        }

        self.create_package_file(
            self.package_name + '/__init__.py', substitutes, self.templates_manager.templates.init_
        )
