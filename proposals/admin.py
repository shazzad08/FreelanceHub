from django.contrib import admin
from .models import Proposal
# Register your models here.

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project_title",
        "freelancer_email",
        "bid_amount",
        "status",
        "created_at",
    )

    @admin.display(description="Project Title")
    def project_title(self, obj):
        return obj.project.title

    @admin.display(description="Freelancer Email")
    def freelancer_email(self, obj):
        return obj.freelancer.email