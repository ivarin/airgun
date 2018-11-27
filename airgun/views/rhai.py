from widgetastic_patternfly import Button
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import (
    Checkbox,
    ParametrizedView,
    Table,
    Text,
    TextInput,
    View
)

from airgun.views.common import BaseLoggedInView
from airgun.widgets import ActionsDropdown, SatTable


class AllRulesView(BaseLoggedInView):
    title = Text(".//h1[normalize-space(.)='Rules']")
    search = TextInput(locator=".//input[@placeholder='Search rules']")

    @property
    def is_displayed(self):
        return self.title.is_displayed and self.search.is_displayed


class InventoryAllHosts(BaseLoggedInView):
    title = Text(".//h1[normalize-space(.)='Inventory']")
    search = TextInput(locator=".//input[@placeholder='Find a system']")
    actions = ActionsDropdown(".//div[contains(@class, 'dropdown')]")
    systems_count = Text(".//h3[@class='system-count']")
    table = SatTable(".//table",
                     column_widgets={"System Name": Text(".//a")})

    @property
    def is_displayed(self):
        return self.title.is_displayed and self.search.is_displayed


class InventoryHostDetails(BaseLoggedInView):
    hostname = Text(".//div[@class='modal-title']/h2/div/span")
    close = Text(".//div[contains(@class, 'fa-close'])")

    @ParametrizedView.nested
    class rules(ParametrizedView):
        PARAMETERS = ("title",)
        ROOT = ParametrizedLocator(
            ".//div[@rule-id='rule_id'][//h3[@class='title' and text()=\"{title}\"]]"
        )
        ALL_RULES = "//div[@rule-id='rule_id']//h3[@class='title']"

        title = Text(".//h3[@class='title']")

        @classmethod
        def all(cls, browser):
            return [(element.text,) for element in browser.elements(cls.ALL_RULES)]

    @property
    def is_displayed(self):
        return self.hostname.is_displayed and self.close.is_displayed


class OverviewDetailsView(BaseLoggedInView):
    title = Text(".//h1[normalize-space(.)='Overview']")
    inventory = Table(".//section[contains(., 'Newest Systems')]//table")
    security_issues = Text(".//div[@ng-if='securityErrors']/div")
    stability_issues = Text(".//div[@ng-if='stabilityErrors']/div")
    inventory_link = Text(".//span[normalize-space(.)='View inventory']")
    actions_link = Text(".//span[normalize-space(.)='View actions']")

    @property
    def is_displayed(self):
        return (
            self.title.is_displayed and
            self.inventory_link.is_displayed and
            self.actions_link.is_displayed
        )


class ActionsDetailsView(BaseLoggedInView):
    title = Text(".//h1[normalize-space(.)='Actions']")
    export_csv = Button("Export CSV")
    stability_issues = Text(".//a[@class='stability']/span[@class='count']")
    security_issues = Text(".//a[@class='security']/span[@class='count']")


class ManageDetailsView(BaseLoggedInView):
    title = Text(".//h1[@class='page-title']")
    enable_service = Checkbox(id="rha-insights-enabled")
    status = Text(".//label[@for='connectionStatus']/parent::div//p")
    account_number = Text(".//label[@for='account']/parent::div//p")
    check_connection = Text(".//input[@value='Check Connection']")
    save = Text(".//input[@value='Save']")


class AllPlansView(BaseLoggedInView):
    title = Text(".//h1[normalize-space(.)='Planner']")
    create_plan = Text(".//a[@class='create-plan']")

    @ParametrizedView.nested
    class plan(ParametrizedView):
        PARAMETERS = ("plan_name", )
        ROOT = ParametrizedLocator(
            ".//h2[contains(normalize-space(.), {plan_name|quote})]/"
            "ancestor::div[contains(@id, 'maintenance-plan')]")

        title = Text(".")
        delete = Text(".//i[@tooltip='Delete this plan']")
        edit = Text(".//i[@tooltip='Click to edit this plan']")
        run_playbook = Button("Run Playbook")
        export_csv = Button("Export CSV")
        add_actions = Button("Add actions")

    @property
    def is_displayed(self):
        return self.title.is_displayed


class PlanEditView(View):
    plan_name = TextInput(name="name")
    date = TextInput(name="date")
    start_time = TextInput(name="time")
    duration = TextInput(name="duration")
    cancel = Button("Cancel")
    save = Button("Save")


class AddPlanView(BaseLoggedInView):
    title = Text(".//h2[normalize-space(.)='Plan / Playbook Builder']")
    name = TextInput(name="name")
    actions = SatTable(
        ".//div[contains(@class, 'maintenance-plan')]//table",
        column_widgets={0: Checkbox(locator=".//input")}
    )
    rules_filter = TextInput(
        locator=".//input[@placeholder='Filter by rule name']")
    cancel = Button("Cancel")
    save = Button("Save")

    @property
    def is_displayed(self):
        return self.title.is_displayed


class PlanModalWindow(View):
    yes = Text(".//button[contains(@class, 'swal2-confirm')]")
    cancel = Text(".//button[contains(@class, 'swal2-cancel')]")
