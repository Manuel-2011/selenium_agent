from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def is_bootstrap_class(input_string):
    bootstrap_classes = {
        "container",
        "row",
        "col",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "lead",
        "text-left",
        "text-right",
        "text-center",
        "text-justify",
        "text-nowrap",
        "btn",
        "btn-primary",
        "btn-secondary",
        "btn-success",
        "btn-danger",
        "btn-warning",
        "btn-info",
        "btn-light",
        "btn-dark",
        "form-group",
        "form-control",
        "form-check",
        "form-check-input",
        "form-check-label",
        "nav",
        "nav-item",
        "nav-link",
        "navbar",
        "navbar-brand",
        "navbar-toggler",
        "modal",
        "modal-dialog",
        "modal-content",
        "modal-header",
        "modal-title",
        "modal-body",
        "modal-footer",
        "carousel",
        "carousel-inner",
        "carousel-item",
        "carousel-control-prev",
        "carousel-control-next",
        "accordion-body",
        "accordion-button",
        "accordion-collapse",
        "accordion-flush",
        "accordion-header",
        "accordion-item",
        "collapsed",
    }

    bootstrap_prefixes = {
        "bs-",
        "bootstrap-",
        "btn-",
        "md:",
        "col-",
        "border-",
        "rounded-",
        "carousel-",
        "bg-",
        "link-",
        "d-",
        "dropdown-",
        "align-content-",
        "align-items-",
        "align-self-",
        "flex-",
        "justify-",
        "order-",
        "form-",
        "row-",
        "g-",
        "container-",
        "gap-",
        "gx-",
        "gy-",
        "offset-",
        "order-",
        "list-",
        "d-",
        "pe-",
        "shadow-",
        "modal-",
        "navbar-",
        "nav-",
        "float-",
        "position-",
        "start-",
        "sticky-",
        "progress-",
        "h-",
        "mh-",
        "w-",
        "m-",
        "me-",
        "ms-",
        "mt-",
        "mx-",
        "my-",
        "p-",
        "pb-",
        "pe-",
        "pl-",
        "ps-",
        "pt-",
        "px-",
        "py-",
        "table-",
        "font-",
        "text-",
        "display-",
        "fs-",
        "fw-",
        "lh-",
        "list-",
        "js-",
    }

    return input_string in bootstrap_classes or any(
        input_string.startswith(prefix) for prefix in bootstrap_prefixes
    )


def is_tailwind_class(class_name):
    tailwind_classes = [
        # Display
        "block",
        "inline",
        "inline-block",
        "hidden",
        "flex",
        "inline-flex",
        # Flex
        "flex-row",
        "flex-row-reverse",
        "flex-col",
        "flex-col-reverse",
        "flex-wrap",
        "flex-wrap-reverse",
        "flex-nowrap",
        "items-start",
        "items-end",
        "items-center",
        "items-baseline",
        "items-stretch",
        "justify-start",
        "justify-end",
        "justify-center",
        "justify-between",
        "justify-around",
        # Typography
        "text-xs",
        "text-sm",
        "text-base",
        "text-lg",
        "text-xl",
        "font-bold",
        "font-semibold",
        "font-normal",
        "font-light",
        "italic",
        "text-left",
        "text-right",
        "text-center",
        "text-justify",
        # Background Colors
        "bg-transparent",
        "bg-black",
        "bg-white",
        "bg-gray-100",
        "bg-red-500",
        "bg-green-500",
        "bg-blue-500",
        "bg-yellow-500",
        "bg-purple-500",
        # Padding & Margin
        "p-4",
        "pt-2",
        "pr-3",
        "pb-4",
        "pl-5",
        "m-4",
        "mt-2",
        "mr-3",
        "mb-4",
        "ml-5",
        # Border
        "border",
        "border-solid",
        "border-gray-500",
        "border-t",
        "border-b",
        "border-r",
        "border-l",
        "border-2",
        "border-transparent",
        "rounded",
        "rounded-lg",
        # Width & Height
        "w-64",
        "h-32",
        "min-w-0",
        "min-h-0",
        # Other
        "shadow",
        "cursor-pointer",
        "transition",
        "ease-in-out",
        "duration-300",
    ]

    return class_name in tailwind_classes


def get_cleaned_classes(class_names):
    distinct_classes = []
    for class_name in class_names:
        similar = False
        if is_bootstrap_class(class_name) or is_tailwind_class(class_name):
            break
        for existing_class in distinct_classes:
            if similarity(class_name, existing_class) >= 0.7:
                similar = True
                break
        if not similar:
            distinct_classes.append(class_name)
    return distinct_classes[:2]


def clean_class_names(tag):
    if "class" in tag.attrs:
        if "id" in tag.attrs:
            del tag["class"]
            return
        class_names = tag.attrs["class"]
        if isinstance(class_names, str):
            class_names = class_names.split()
        elif isinstance(class_names, list):
            class_names = " ".join(class_names).split()
        tag.attrs["class"] = get_cleaned_classes(class_names)


def remove_extra_info(html):
    # Create BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Remove specific tags or elements
    unwanted_tags = [
        "script",
        "style",
        "meta",
        "link",
        "iframe",
        "svg",
        "head",
        "span",
        "code",
        "no-script",
    ]
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.extract()

    # Remove extra attributes from tags
    essential_attributes = ["id", "class", "href", "src"]
    for tag in soup(recursive=True):
        clean_class_names(tag)
        extra_attributes = [
            attr for attr in tag.attrs if attr not in essential_attributes
        ]
        for attr in extra_attributes:
            del tag[attr]

    # Return the cleaned HTML
    return str(soup)


def remove_blank_lines(content):
    # Split the content into lines, then filter out empty lines
    lines = filter(lambda line: line.strip(), content.splitlines())
    # Join the non-empty lines back together
    return "\n".join(lines)


def store_string_to_txt(filename, content):
    try:
        # Open the file in write mode
        with open(filename, "w") as file:
            # Write the content to the file
            file.write(content)
        print("String has been successfully stored in", filename)
    except Exception as e:
        print("An error occurred:", str(e))


def get_cleaned_html(raw_html):
    cleaned_html = remove_extra_info(raw_html)
    cleaned_html = remove_blank_lines(cleaned_html)
    store_string_to_txt("cleaned_html", cleaned_html)
    return cleaned_html
