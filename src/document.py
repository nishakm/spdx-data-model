# Copyright 2020 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause

"""
This file contains a python implementation of the SPDX document model
"""
from enum import Enum
from enum import auto
from abc import ABC
from abc import abstractmethod


class IntegrityMethod(ABC):
    """SPDX Element integrity verification method
    Derived class must implement the methods
    generate and verify"""
    @abstractmethod
    def generate(self, **kwargs):
        pass

    @abstractmethod
    def verify(self, **kwargs):
        pass


class Hash(IntegrityMethod):
    """Hashing algorithm"""
    def __init__(self,
                 algo="",
                 value=""):
        self.HashAlgorithm = algo
        self.Value = value

    def generate(self):
        return ""

    def verify(self, value=""):
        return value


class ExternalReference:
    """References to other locations
    uri's package manager, pointers to anything"""
    def __init__(self,
                 category="",
                 reftype="",
                 locator="",
                 comment=""):
        self.Category = category
        self.Type = reftype
        self.Locator = locator  # python has a URI module that could be useful
        self.Comment = comment


class SpdxDocumentReference:
    """Basic SPDX External Document Reference
    specific to referencing SPDX element in a separate SPDX document"""
    def __init__(self,
                 document_ref="",
                 locator="",
                 verification=IntegrityMethod):
        self.DocumentRef = document_ref
        self.Locator = locator
        self.VerifiedWith = verification


class SpdxElement:
    """ SpdxElement is base class of SPDX objects"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod):
        self.SPDXID = ""
        self.Name = name
        self.Summary = summary
        self.Description = description
        self.Comment = comment
        self.VerifiedWith = verification


class RelationshipType(Enum):
    """The RelationshipType object describes the type of relationship between
    two SpdxElements"""
    DESCRIBES = auto()
    DESCRIBED_BY = auto()
    CONTAINS = auto()
    CONTAINED_BY = auto()
    DEPENDS_ON = auto()
    DEPENDENCY_OF = auto()
    DEPENDENCY_MANIFEST_OF = auto()
    BUILD_DEPENDENCY_OF = auto()
    DEV_DEPENDENCY_OF = auto()
    OPTIONAL_DEPENDENCY_OF = auto()
    PROVIDED_DEPENDENCY_OF = auto()
    TEST_DEPENDENCY_OF = auto()
    RUNTIME_DEPENDENCY_OF = auto()
    EXAMPLE_OF = auto()
    GENERATES = auto()
    GENERATED_FROM = auto()


class Relationship(SpdxElement):
    """Relationship describes the relationship between two SPDX objects"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 relationship_type=RelationshipType,
                 from_element=SpdxElement,
                 to_element=SpdxElement):
        super().__init__(name, summary, description, comment, verification)
        self.RelationshipType = relationship_type
        self.From = from_element
        self.To = to_element
        self.VerfiedWith = verification
        # question: should To be more than one?


class Identity(SpdxElement):
    """Identity of the entities involved"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 email=""):
        super().__init__(name, summary, description, comment, verification)
        self.Email = email
        # question: why separate person, organization, or tool?


class SpdxDocument(SpdxElement):
    """SpdxDocument is the document level object"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 namespace="",
                 created="",
                 creator=Identity,
                 external_document_references=[SpdxDocumentReference],
                 profiles=[]):
        super().__init__(name, summary, description, comment, verification)
        self.SPDXVersion = 3.0
        self.DataLicense = 3.0
        self.Namespace = namespace
        self.Created = created
        self.Creator = creator
        self.ExternalDocumentReferences = external_document_references
        self.Profiles = profiles


class Artifact(SpdxElement):
    """Artifact describes the artifact being distributed"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 artifact_url="",
                 supplier=Identity,
                 originator=Identity,
                 external_references=[ExternalReference]):
        super().__init__(name, summary, description, comment, verification)
        self.ArtifactUrl = artifact_url
        self.Supplier = supplier
        self.Originator = originator
        self.ExternalReferences = external_references


class Package(Artifact):
    """Package is a type of artifact"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 artifact_url="",
                 supplier=Identity,
                 originator=Identity,
                 external_references=[ExternalReference],
                 version=""):
        # suggest moving version string to Artifact
        super().__init__(name,
                         summary,
                         description,
                         comment,
                         verification,
                         artifact_url,
                         supplier,
                         originator,
                         external_references)
        self.Version = version


class File(Artifact):
    """File is a type of artifact"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 artifact_url="",
                 supplier=Identity,
                 originator=Identity,
                 external_references=[ExternalReference],
                 file_type=""):
        # suggest moving version string to Artifact
        super().__init__(name,
                         summary,
                         description,
                         comment,
                         verification,
                         artifact_url,
                         supplier,
                         originator,
                         external_references)
        self.FileType = file_type


class Snippet(Artifact):
    """Snippet is a type of artifact"""
    def __init__(self,
                 name="",
                 summary="",
                 description="",
                 comment="",
                 verification=IntegrityMethod,
                 artifact_url="",
                 supplier=Identity,
                 originator=Identity,
                 external_references=[ExternalReference],
                 byte_range=0,
                 line_range=0):
        # suggest moving version string to Artifact
        super().__init__(name,
                         summary,
                         description,
                         comment,
                         verification,
                         artifact_url,
                         supplier,
                         originator,
                         external_references)
        self.ByteRange = byte_range
        self.LineRange = line_range
