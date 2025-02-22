from .logging import log

try:
    import gallery_dl.formatter as formatter
except ImportError:
    pass


def format_impl(format_str: str, *args, **kwargs: dict[str, str | int]):
    if formatter is not None:
        if '{}' in format_str:
            # TODO: handle {} with slices, other operations?
            log.warning('Replacing {} with {fullname} for gallery_dl compat')
            format_str = format_str.replace('{}', '{fullname}')
        fmt: formatter.StringFormatter = formatter.parse(format_str)
        return fmt.format_map(kwargs)
    return format_str.format(*args, **kwargs)
