from typing import List, Optional, Dict, Any
from datetime import datetime

class User:
    """Class representing a user in Asana"""
    def __init__(self, gid: str, name: str, resource_type: str = "user"):
        self.gid = gid
        self.name = name
        self.resource_type = resource_type

class EnumOption:
    """Class representing an enum option in custom fields"""
    def __init__(self, gid: str, color: str, enabled: bool, name: str, resource_type: str = "enum_option"):
        self.gid = gid
        self.color = color
        self.enabled = enabled
        self.name = name
        self.resource_type = resource_type

class CustomField:
    """Class representing a custom field"""
    def __init__(self, gid: str, enabled: bool, name: str, description: str = "", 
                 resource_subtype: str = "", resource_type: str = "custom_field",
                 is_formula_field: bool = False, is_value_read_only: bool = False,
                 field_type: str = "", enum_options: List[EnumOption] = None,
                 multi_enum_values: List = None, display_value: Any = None,
                 created_by: User = None):
        self.gid = gid
        self.enabled = enabled
        self.name = name
        self.description = description
        self.resource_subtype = resource_subtype
        self.resource_type = resource_type
        self.is_formula_field = is_formula_field
        self.is_value_read_only = is_value_read_only
        self.type = field_type
        self.enum_options = enum_options or []
        self.multi_enum_values = multi_enum_values or []
        self.display_value = display_value
        self.created_by = created_by

class Project:
    """Class representing a project in Asana"""
    def __init__(self, gid: str, name: str, resource_type: str = "project"):
        self.gid = gid
        self.name = name
        self.resource_type = resource_type

class Section:
    """Class representing a section in Asana"""
    def __init__(self, gid: str, name: str, resource_type: str = "section"):
        self.gid = gid
        self.name = name
        self.resource_type = resource_type

class Membership:
    """Class representing a membership (project and section)"""
    def __init__(self, project: Project = None, section: Section = None):
        self.project = project
        self.section = section

class Task:
    """Class representing a Task in Asana with support for nested subtasks"""
    
    def __init__(self, gid: str, name: str, completed: bool = False,
                 actual_time_minutes: Optional[int] = None,
                 assignee: Optional[User] = None,
                 assignee_status: str = "upcoming",
                 completed_at: Optional[str] = None,
                 created_at: Optional[str] = None,
                 custom_fields: List[CustomField] = None,
                 due_at: Optional[str] = None,
                 due_on: Optional[str] = None,
                 followers: List[User] = None,
                 hearted: bool = False,
                 hearts: List = None,
                 liked: bool = False,
                 likes: List = None,
                 memberships: List[Membership] = None,
                 modified_at: Optional[str] = None,
                 notes: str = "",
                 num_hearts: int = 0,
                 num_likes: int = 0,
                 parent: Optional['Task'] = None,
                 permalink_url: str = "",
                 projects: List = None,
                 resource_type: str = "task",
                 start_at: Optional[str] = None,
                 start_on: Optional[str] = None,
                 subtasks: List['Task'] = None):
        
        self.gid = gid
        self.actual_time_minutes = actual_time_minutes
        self.assignee = assignee
        self.assignee_status = assignee_status
        self.completed = completed
        self.completed_at = completed_at
        self.created_at = created_at
        self.custom_fields = custom_fields or []
        self.due_at = due_at
        self.due_on = due_on
        self.followers = followers or []
        self.hearted = hearted
        self.hearts = hearts or []
        self.liked = liked
        self.likes = likes or []
        self.memberships = memberships or []
        self.modified_at = modified_at
        self.name = name
        self.notes = notes
        self.num_hearts = num_hearts
        self.num_likes = num_likes
        self.parent = parent
        self.permalink_url = permalink_url
        self.projects = projects or []
        self.resource_type = resource_type
        self.start_at = start_at
        self.start_on = start_on
        self.subtasks = subtasks or []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary (e.g., from JSON)"""
        
        # Parse assignee
        assignee = None
        if data.get('assignee'):
            assignee_data = data['assignee']
            assignee = User(
                gid=assignee_data.get('gid', ''),
                name=assignee_data.get('name', ''),
                resource_type=assignee_data.get('resource_type', 'user')
            )
        
        # Parse followers
        followers = []
        for follower_data in data.get('followers', []):
            followers.append(User(
                gid=follower_data.get('gid', ''),
                name=follower_data.get('name', ''),
                resource_type=follower_data.get('resource_type', 'user')
            ))
        
        # Parse custom fields
        custom_fields = []
        for cf_data in data.get('custom_fields', []):
            # Parse enum options
            enum_options = []
            for enum_data in cf_data.get('enum_options', []):
                enum_options.append(EnumOption(
                    gid=enum_data.get('gid', ''),
                    color=enum_data.get('color', ''),
                    enabled=enum_data.get('enabled', True),
                    name=enum_data.get('name', ''),
                    resource_type=enum_data.get('resource_type', 'enum_option')
                ))
            
            # Parse created_by user
            created_by = None
            if cf_data.get('created_by'):
                cb_data = cf_data['created_by']
                created_by = User(
                    gid=cb_data.get('gid', ''),
                    name=cb_data.get('name', ''),
                    resource_type=cb_data.get('resource_type', 'user')
                )
            
            custom_fields.append(CustomField(
                gid=cf_data.get('gid', ''),
                enabled=cf_data.get('enabled', True),
                name=cf_data.get('name', ''),
                description=cf_data.get('description', ''),
                resource_subtype=cf_data.get('resource_subtype', ''),
                resource_type=cf_data.get('resource_type', 'custom_field'),
                is_formula_field=cf_data.get('is_formula_field', False),
                is_value_read_only=cf_data.get('is_value_read_only', False),
                field_type=cf_data.get('type', ''),
                enum_options=enum_options,
                multi_enum_values=cf_data.get('multi_enum_values', []),
                display_value=cf_data.get('display_value'),
                created_by=created_by
            ))
        
        # Parse memberships
        memberships = []
        for membership_data in data.get('memberships', []):
            project = None
            section = None
            
            # Parse project
            if membership_data.get('project'):
                project_data = membership_data['project']
                project = Project(
                    gid=project_data.get('gid', ''),
                    name=project_data.get('name', ''),
                    resource_type=project_data.get('resource_type', 'project')
                )
            
            # Parse section
            if membership_data.get('section'):
                section_data = membership_data['section']
                section = Section(
                    gid=section_data.get('gid', ''),
                    name=section_data.get('name', ''),
                    resource_type=section_data.get('resource_type', 'section')
                )
            
            memberships.append(Membership(project=project, section=section))        
        # Parse parent task
        parent = None
        if data.get('parent'):
            parent = cls.from_dict(data['parent'])
        
        # Parse subtasks recursively
        subtasks = []
        for subtask_data in data.get('subtasks', []):
            subtasks.append(cls.from_dict(subtask_data))
        
        return cls(
            gid=data.get('gid', ''),
            name=data.get('name', ''),
            completed=data.get('completed', False),
            actual_time_minutes=data.get('actual_time_minutes'),
            assignee=assignee,
            assignee_status=data.get('assignee_status', 'upcoming'),
            completed_at=data.get('completed_at'),
            created_at=data.get('created_at'),
            custom_fields=custom_fields,
            due_at=data.get('due_at'),
            due_on=data.get('due_on'),
            followers=followers,
            hearted=data.get('hearted', False),
            hearts=data.get('hearts', []),
            liked=data.get('liked', False),
            likes=data.get('likes', []),
            memberships=memberships,
            modified_at=data.get('modified_at'),
            notes=data.get('notes', ''),
            num_hearts=data.get('num_hearts', 0),
            num_likes=data.get('num_likes', 0),
            parent=parent,
            permalink_url=data.get('permalink_url', ''),
            projects=data.get('projects', []),
            resource_type=data.get('resource_type', 'task'),
            start_at=data.get('start_at'),
            start_on=data.get('start_on'),
            subtasks=subtasks
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Task instance to dictionary"""
        result = {
            'gid': self.gid,
            'actual_time_minutes': self.actual_time_minutes,
            'assignee': self.assignee.__dict__ if self.assignee else None,
            'assignee_status': self.assignee_status,
            'completed': self.completed,
            'completed_at': self.completed_at,
            'created_at': self.created_at,
            'custom_fields': [cf.__dict__ for cf in self.custom_fields],
            'due_at': self.due_at,
            'due_on': self.due_on,
            'followers': [f.__dict__ for f in self.followers],
            'hearted': self.hearted,
            'hearts': self.hearts,
            'liked': self.liked,
            'likes': self.likes,
            'memberships': [
                {
                    'project': membership.project.__dict__ if membership.project else None,
                    'section': membership.section.__dict__ if membership.section else None
                }
                for membership in self.memberships
            ],
            'modified_at': self.modified_at,
            'name': self.name,
            'notes': self.notes,
            'num_hearts': self.num_hearts,
            'num_likes': self.num_likes,
            'parent': self.parent.to_dict() if self.parent else None,
            'permalink_url': self.permalink_url,
            'projects': self.projects,
            'resource_type': self.resource_type,
            'start_at': self.start_at,
            'start_on': self.start_on,
            'subtasks': [subtask.to_dict() for subtask in self.subtasks]
        }
        return result
    
    def add_subtask(self, subtask: 'Task'):
        """Add a subtask to this task"""
        subtask.parent = self
        self.subtasks.append(subtask)
    
    def get_all_subtasks(self) -> List['Task']:
        """Get all subtasks recursively (including nested subtasks)"""
        all_subtasks = []
        for subtask in self.subtasks:
            all_subtasks.append(subtask)
            all_subtasks.extend(subtask.get_all_subtasks())
        return all_subtasks
    
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.completed
    
    def has_subtasks(self) -> bool:
        """Check if task has subtasks"""
        return len(self.subtasks) > 0
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage based on subtasks"""
        if not self.has_subtasks():
            return 100.0 if self.completed else 0.0
        
        completed_subtasks = sum(1 for subtask in self.subtasks if subtask.completed)
        return (completed_subtasks / len(self.subtasks)) * 100.0
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"{status} {self.name} (ID: {self.gid})"
    
    def __repr__(self) -> str:
        return f"Task(gid='{self.gid}', name='{self.name}', completed={self.completed}, subtasks_count={len(self.subtasks)})"
    
    def get_projects(self) -> List[Project]:
        """Get all projects this task belongs to"""
        projects = []
        for membership in self.memberships:
            if membership.project:
                projects.append(membership.project)
        return projects
    
    def get_sections(self) -> List[Section]:
        """Get all sections this task belongs to"""
        sections = []
        for membership in self.memberships:
            if membership.section:
                sections.append(membership.section)
        return sections
    
    def get_project_names(self) -> List[str]:
        """Get names of all projects this task belongs to"""
        return [project.name for project in self.get_projects()]
    
    def get_section_names(self) -> List[str]:
        """Get names of all sections this task belongs to"""
        return [section.name for section in self.get_sections()]
