package com.cinebuscador.config;

import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.SimpleEvaluationContext;
import org.springframework.stereotype.Component;


@Component
public class SpelEvaluator {


    public String evaluate(String expression) {
        if (expression == null || expression.isBlank()) {
            return "";
        }

        ExpressionParser parser = new SpelExpressionParser();

        org.springframework.expression.EvaluationContext context =
            SimpleEvaluationContext.forReadOnlyDataBinding().build();

        var expr = parser.parseExpression(expression);
        Object result = expr.getValue(context);

        return result != null ? result.toString() : "";
    }
}
