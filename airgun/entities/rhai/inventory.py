from airgun.entities.base import BaseEntity
from airgun.navigation import NavigateStep, navigator
from airgun.views.rhai import InventoryAllHosts, InventoryHostDetails
from wait_for import wait_for


class InventoryHostEntity(BaseEntity):

    @property
    def total_systems(self):
        """Get number of all systems."""
        view = self.navigate_to(self, "All")
        return view.systems_count.text.split()[0]

    def search(self, host_name):
        """Search a certain host."""
        view = self.navigate_to(self, "All")
        view.search.fill(host_name)
        return view.table

    def read(self, entity_name):
        view = self.navigate_to(self, "Details", entity_name=entity_name)
        wait_for(lambda: bool(view.read()['rules']) is True)
        return view.read()


@navigator.register(InventoryHostEntity, "All")
class AllHosts(NavigateStep):
    """Navigate to Insights Inventory screen."""
    VIEW = InventoryAllHosts

    def step(self, *args, **kwargs):
        self.view.menu.select("Insights", "Inventory")


@navigator.register(InventoryHostEntity, "Details")
class HostDetails(NavigateStep):
    """Navigate to Insights Inventory screen.

    Args:
        entity_name: hostname
    """
    VIEW = InventoryHostDetails

    def prerequisite(self, *args, **kwargs):
        return self.navigate_to(self.obj, "All")

    def step(self, *args, **kwargs):
        self.parent.search.fill(kwargs["entity_name"])
        self.parent.table[0]["System Name"].widget.click()
