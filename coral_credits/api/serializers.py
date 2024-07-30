from rest_framework import serializers

from coral_credits.api import models
from coral_credits.api.business_objects import (
    Allocation,
    ConsumerRequest,
    Context,
    Lease,
    Reservation,
    ResourceRequest,
)


class ResourceClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ResourceClass
        fields = ["id", "url", "name", "created"]


class ResourceProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ResourceProvider
        fields = ["id", "url", "name", "created", "email", "info_url"]


class ResourceProviderAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ResourceProviderAccount
        fields = ["id", "url", "account", "provider", "project_id"]


class CreditAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CreditAccount
        fields = ["id", "url", "name", "email", "created"]


class CreditAllocationResourceSerializer(serializers.ModelSerializer):
    resource_class = ResourceClassSerializer()
    resource_hours = serializers.FloatField()

    class Meta:
        model = models.CreditAllocationResource
        fields = ["resource_class", "resource_hours"]

    def to_representation(self, instance):
        """Pass the context to the ResourceClassSerializer"""
        representation = super().to_representation(instance)
        resource_class_serializer = ResourceClassSerializer(
            instance.resource_class, context=self.context
        )
        representation["resource_class"] = resource_class_serializer.data
        return representation


class CreditAllocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CreditAllocation
        fields = ["id", "name", "created", "account", "start", "end"]


class ResourceConsumptionRecord(serializers.ModelSerializer):
    resource_class = ResourceClassSerializer()

    class Meta:
        model = models.ResourceConsumptionRecord
        fields = ["resource_class", "resource_hours"]


class Consumer(serializers.ModelSerializer):
    resource_provider = ResourceProviderSerializer()
    resources = ResourceConsumptionRecord(many=True)

    class Meta:
        model = models.Consumer
        fields = ["consumer_ref", "resource_provider", "start", "end", "resources"]


class ResourceRequestSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.resources

    def to_internal_value(self, data):
        return {"resources": data}

    def create(self, validated_data):
        return ResourceRequest(**validated_data)


class AllocationSerializer(serializers.Serializer):
    id = serializers.CharField()
    hypervisor_hostname = serializers.CharField()
    extra = serializers.DictField(required=False, allow_null=True)

    def create(self, validated_data):
        return Allocation(
            id=validated_data["id"],
            hypervisor_hostname=validated_data["hypervisor_hostname"],
            extra=validated_data.get("extra", {}),
        )


class ReservationSerializer(serializers.Serializer):
    resource_type = serializers.CharField()
    min = serializers.IntegerField()
    max = serializers.IntegerField()
    hypervisor_properties = serializers.CharField(required=False, allow_null=True)
    resource_properties = serializers.CharField(required=False, allow_null=True)
    allocations = serializers.ListField(
        child=AllocationSerializer(), required=False, allow_null=True
    )

    def create(self, validated_data):
        allocations = [
            AllocationSerializer().create(alloc)
            for alloc in validated_data.get("allocations", [])
        ]
        return Reservation(
            **validated_data,
            allocations=allocations,
        )


class LeaseSerializer(serializers.Serializer):
    def __init__(self, *args, dry_run=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional field id
        self.fields["id"] = serializers.UUIDField(
            required=(not dry_run), allow_null=dry_run
        )

    name = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    before_end_date = serializers.DateTimeField(required=False, allow_null=True)
    reservations = serializers.ListField(child=ReservationSerializer())
    resource_requests = ResourceRequestSerializer()

    def create(self, validated_data):
        reservations = [
            ReservationSerializer().create(res)
            for res in validated_data.pop("reservations")
        ]
        resource_requests = ResourceRequestSerializer().create(
            validated_data.pop("resource_requests")
        )
        return Lease(
            id=validated_data["id"],
            name=validated_data["name"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            reservations=reservations,
            resource_requests=resource_requests,
        )


class ContextSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    project_id = serializers.UUIDField()
    auth_url = serializers.URLField()
    region_name = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        return Context(
            user_id=validated_data["user_id"],
            project_id=validated_data["project_id"],
            auth_url=validated_data["auth_url"],
            region_name=validated_data["region_name"],
        )


class ConsumerRequestSerializer(serializers.Serializer):
    def __init__(self, *args, current_lease_required=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional field current_lease
        self.fields["current_lease"] = LeaseSerializer(
            required=current_lease_required, allow_null=(not current_lease_required)
        )

    context = ContextSerializer()
    lease = LeaseSerializer()

    def create(self, validated_data):
        context = ContextSerializer().create(validated_data["context"])
        lease = LeaseSerializer().create(validated_data["lease"])
        current_lease = (
            LeaseSerializer().create(validated_data["current_lease"])
            if "current_lease" in validated_data
            else None
        )
        return ConsumerRequest(
            context=context, lease=lease, current_lease=current_lease
        )

    def to_internal_value(self, data):
        # Custom validation or processing can be added here if needed
        return super().to_internal_value(data)

    def to_representation(self, instance):
        # Custom representation logic can be added here if needed
        return super().to_representation(instance)
