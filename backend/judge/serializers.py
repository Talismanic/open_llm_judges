from rest_framework import serializers

class WorkerAgentModelSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    endpoint = serializers.URLField()
    api_key = serializers.CharField(required=False, allow_blank=True)  # Optional API key

class JudgeRequestSerializer(serializers.Serializer):
    archetype = serializers.IntegerField()
    num_agents = serializers.IntegerField(required=False, default=1)  # Optional, default=1
    task_meta = serializers.CharField()  # Ensuring task_meta is a string
    task = serializers.CharField()
    worker_agent_models = WorkerAgentModelSerializer(many=True)  # Accepts an array of objects

    def validate(self, data):
        archetype = data.get("archetype")
        num_agents = data.get("num_agents", 1)
        worker_agent_models = data.get("worker_agent_models")

        # Archetype 1: num_agents should always be 1
        if archetype == 1:
            data["num_agents"] = 1  # Force it to be 1
            if len(worker_agent_models) != 1:
                raise serializers.ValidationError("For archetype=1, worker_agent_models must contain exactly 1 entry.")

        # Archetype 2: num_agents must be provided and match the worker_agent_models length
        elif archetype == 2:
            if "num_agents" not in data:
                raise serializers.ValidationError("For archetype=2, num_agents must be provided.")
            if len(worker_agent_models) != num_agents:
                raise serializers.ValidationError("For archetype=2, worker_agent_models length must match num_agents.")

        # Archetype 3: num_agents must be odd and match the worker_agent_models length
        elif archetype == 3:
            if "num_agents" not in data:
                raise serializers.ValidationError("For archetype=3, num_agents must be provided.")
            if num_agents % 2 == 0:
                raise serializers.ValidationError("For archetype=3, num_agents must be an odd number.")
            if len(worker_agent_models) != num_agents:
                raise serializers.ValidationError("For archetype=3, worker_agent_models length must match num_agents.")

        return data
