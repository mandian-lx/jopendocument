%{?_javapackages_macros:%_javapackages_macros}

%define oname jOpenDocument
%define name %(echo %oname | tr [:upper:] [:lower:])

Summary:	A pure Java library for OASIS Open Document files manipulation
Name:		%{name}
Version:	1.3
Release:	1
License:	GPLv3+
Group:		Development/Java
URL:		https://jopendocument.org
Source0:	https://jopendocument.org/download/%{oname}-src-%{version}.zip
Source1:	https://repo1.maven.org/maven2/org/%{name}/%{oname}/%{version}/%{oname}-%{version}.pom
Patch0:		%{name}-1.3-ognl.patch
Patch1:		%{name}-1.3-port-to-java8.patch
Patch2:		%{name}-1.3-port-to-commons-collections4.patch
BuildArch:	noarch

BuildRequires:	javapackages-tools
BuildRequires:	ant
BuildRequires:	maven-local
BuildRequires:	apache-commons-collections4
BuildRequires:	apache-commons-ognl
BuildRequires:	isorelax
BuildRequires:	itext
BuildRequires:	jaxen
BuildRequires:	jcip-annotations
BuildRequires:	jdom
BuildRequires:	js
BuildRequires:	junit


%description
jOpenDocument is a free library for developers looking to use Open Document
files without OpenOffice.org.

You can automate the document creation and manipulation process. You can use
jOpenDocument to:

    - Generate dynamic documents from Java, XML or databases
    - Display and print files with built-in viewers
    - Split, concatenate, and manipulate pages
    - Automate filling out of template (created by OpenOffice or not)
    - Use your preferred langage via standard ScriptEngine interface
    - And much more...

%files -f .mfiles
%dir %{_javadir}/%{name}
%dir %{_mavenpomdir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/template/
%doc README
%doc NEWS
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

#----------------------------------------------------------------------------

%prep
%setup -q -c %{name}-%{version}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 -b .jdk8
%patch2 -p1 -b .collections4

# Add pom.xml file
cp %{SOURCE1} pom.xml

# Set classpath
build-jar-repository ./lib commons-collections4 commons-ognl isorelax itext jaxen jcip-annotations jdom js junit

%build
export ANT_OPTS=' -Dfile.encoding=UTF-8 -Djavadoc.encoding=ISO-8859-1 -Djavadoc.docencoding=UTF-8'

# jar
%ant

# docs
%javadoc \
	-encoding ISO-8859-1 -docencoding UTF-8 \
	-classpath `build-classpath commons-collections4 commons-ognl isorelax itext jaxen jcip-annotations jdom js junit` \
	-d doc -public \
	`find ./src -name '*.java'`

# maven artifact
%mvn_artifact pom.xml dist/%{oname}-%{version}.jar

%install
%mvn_install -J doc

# template
install -dm 0755 %{buildroot}%{_datadir}/%{name}/template/
install -pm 0644 template/* %{buildroot}%{_datadir}/%{name}/template/

