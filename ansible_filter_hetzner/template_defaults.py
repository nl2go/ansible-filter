#!/usr/bin/python


TEMPLATE_DEFAULTS = {
    'whitelist_hos': False,
    'is_default': False
}

RULE_DEFAULTS = {
    'ip_version': 'ipv4'
}


def template_defaults(templates):
    result_templates = []
    for template in templates:
        result_template = {}
        result_template.update(TEMPLATE_DEFAULTS)
        result_template.update(template)
        result_template['rules'] = rule_defaults(template.get('rules'))

        result_templates.append(result_template)

    return result_templates


def rule_defaults(rules):
    if rules:
        result_rules = {}
        for chain, chain_rules in rules.items():
            if chain_rules:
                result_chain_rules = []
                for chain_rule in chain_rules:
                    result_chain_rule = {}
                    result_chain_rule.update(RULE_DEFAULTS)
                    result_chain_rule.update(chain_rule)
                    result_chain_rules.append(result_chain_rule)

                result_rules[chain] = result_chain_rules
        return result_rules
    return {}
